import os
import json

from dotenv import load_dotenv
from google import genai

from models.schemas import CivicIssueAnalysis


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GEMMA_API_KEY = os.getenv("GEMMA_API_KEY")

if not GEMMA_API_KEY:
    raise ValueError("GEMMA_API_KEY is not configured.")


# ============================================================
# GEMMA CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMMA_API_KEY
)

GEMMA_MODEL = "gemma-4-26b-a4b-it"


# ============================================================
# CIVIC ISSUE ANALYSIS
# ============================================================

def analyze_civic_issue(
    image_bytes: bytes,
    mime_type: str,
    description: str = "",
    location: str = ""
) -> CivicIssueAnalysis:

    prompt = f"""
You are CiviSense AI.

You analyze photographs of civic and public infrastructure
problems and help citizens understand what action should be
taken.

Analyze the provided image carefully.

CITIZEN DESCRIPTION:
{description if description else "No description provided."}

LOCATION:
{location if location else "Location not provided."}


============================================================
ISSUE CLASSIFICATION
============================================================

You MUST classify the issue using exactly ONE of these
issue codes:

ROAD_POTHOLE
BROKEN_STREETLIGHT
ELECTRICAL_HAZARD
GARBAGE_ACCUMULATION
BLOCKED_DRAIN
WATER_LEAKAGE
FALLEN_TREE
TRAFFIC_OBSTRUCTION
PUBLIC_INFRASTRUCTURE_DAMAGE
OTHER_CIVIC_ISSUE


CLASSIFICATION GUIDANCE

ROAD_POTHOLE:
Potholes, road surface damage, major road cracks,
road depressions.

BROKEN_STREETLIGHT:
Broken, damaged, fallen, or non-functional public
streetlights.

ELECTRICAL_HAZARD:
Exposed electrical wires, fallen electrical wires,
dangerously hanging wires, visible electrical hazards.

GARBAGE_ACCUMULATION:
Accumulated garbage, public waste, illegal dumping,
trash piles.

BLOCKED_DRAIN:
Blocked drains, overflowing drains, open or damaged
public drainage.

WATER_LEAKAGE:
Visible water pipeline leakage or damaged public
water infrastructure.

FALLEN_TREE:
Fallen trees, large fallen branches, trees blocking
public roads.

TRAFFIC_OBSTRUCTION:
Objects, debris, vehicles, or infrastructure visibly
blocking public traffic.

PUBLIC_INFRASTRUCTURE_DAMAGE:
Damaged public infrastructure that does not clearly
belong to another category.

OTHER_CIVIC_ISSUE:
Use this ONLY when none of the above categories
reasonably describe the visible issue.


============================================================
SEVERITY
============================================================

Rate the issue from 0 to 10.

0-2   = Minor
3-5   = Moderate
6-7   = Serious
8-10  = Critical


Consider:

- Immediate danger to people
- Risk to road users
- Risk of electrical injury
- Risk of accidents
- Size and extent of damage
- Whether the issue appears to affect public access
- Potential escalation if left unresolved


============================================================
IMPORTANT RULES
============================================================

- Only identify things reasonably supported by the image.
- Do not invent facts.
- Do not invent phone numbers.
- Do not invent email addresses.
- Do not invent government websites.
- Do not claim exact technical specifications that
  cannot be determined from the image.
- Clearly distinguish visible evidence from assumptions.
- If something cannot be determined from the image,
  say that verification is required.


============================================================
OUTPUT
============================================================

Return ONLY valid JSON.

Use exactly this structure:

{{
    "issue_code": "ROAD_POTHOLE",

    "issue": "Pothole",

    "category": "Road Infrastructure",

    "severity": {{
        "score": 8.0,
        "level": "Critical",
        "urgency": "High"
    }},

    "visible_evidence": [
        "Large depression visible in the road surface"
    ],

    "potential_risks": [
        "Risk to vehicles",
        "Risk to two-wheelers"
    ],

    "recommended_authority": {{
        "authority_type": "Municipal Corporation / Road Authority",
        "department": "Road Maintenance Department"
    }},

    "citizen_instructions": [
        "Record the exact location",
        "Include the photograph when reporting"
    ],

    "required_report_information": [
        "Exact location",
        "Date and time",
        "Photograph"
    ],

    "complaint_subject": "Complaint regarding road pothole",

    "complaint_letter": "Formal complaint letter..."
}}
"""

    # ========================================================
    # CALL GEMMA
    # ========================================================

    response = client.models.generate_content(
        model=GEMMA_MODEL,
        contents=[
            {
                "text": prompt
            },
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_bytes
                }
            }
        ]
    )

    # ========================================================
    # EXTRACT RESPONSE
    # ========================================================

    raw_response = response.text.strip()

    # Remove markdown code fences if Gemma happens to return them
    if raw_response.startswith("```json"):
        raw_response = raw_response[7:]

    elif raw_response.startswith("```"):
        raw_response = raw_response[3:]

    if raw_response.endswith("```"):
        raw_response = raw_response[:-3]

    raw_response = raw_response.strip()

    # ========================================================
    # PARSE JSON
    # ========================================================

    try:
        data = json.loads(raw_response)

    except json.JSONDecodeError as e:

        print("Gemma returned invalid JSON:")
        print(raw_response)

        raise ValueError(
            f"Gemma returned invalid JSON: {e}"
        )

    # ========================================================
    # VALIDATE WITH PYDANTIC
    # ========================================================

    try:

        analysis = CivicIssueAnalysis.model_validate(data)

    except Exception as e:

        print("Gemma JSON failed schema validation:")
        print(data)

        raise ValueError(
            f"Gemma response does not match schema: {e}"
        )

    return analysis