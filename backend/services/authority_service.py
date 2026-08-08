import json
from pathlib import Path
from typing import Optional


# ============================================================
# DATA FILES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

AUTHORITY_FILE = BASE_DIR / "data" / "authorities.json"
ISSUE_CODE_FILE = BASE_DIR / "data" / "issue_codes.json"


# ============================================================
# LOAD DATA
# ============================================================

def load_json_file(path: Path) -> dict:

    if not path.exists():
        raise FileNotFoundError(
            f"Data file not found: {path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


AUTHORITIES = load_json_file(AUTHORITY_FILE)

ISSUE_CODES = load_json_file(ISSUE_CODE_FILE)


# ============================================================
# ISSUE CODE LOOKUP
# ============================================================

def get_issue_definition(
    issue_code: str
) -> Optional[dict]:
    """
    Get the definition of a canonical issue code.
    """

    return ISSUE_CODES.get(issue_code)


# ============================================================
# AUTHORITY LOOKUP
# ============================================================

def get_authority_by_issue_code(
    issue_code: str
) -> dict:
    """
    Resolve a canonical issue code to an authority.

    Gemma supplies the issue_code.
    Python performs the deterministic lookup.
    """

    issue_definition = get_issue_definition(
        issue_code
    )

    # --------------------------------------------------------
    # Unknown issue code
    # --------------------------------------------------------

    if issue_definition is None:

        return {
            "matched": False,
            "issue_code": issue_code,
            "authority": None,
            "message": (
                "Unknown issue code. "
                "Manual authority verification required."
            )
        }

    # --------------------------------------------------------
    # No authority mapping
    # --------------------------------------------------------

    authority_id = issue_definition.get(
        "authority_id"
    )

    if not authority_id:

        return {
            "matched": False,
            "issue_code": issue_code,
            "authority": None,
            "message": (
                "This issue does not have a predefined "
                "authority mapping."
            )
        }

    # --------------------------------------------------------
    # Exact authority lookup
    # --------------------------------------------------------

    authority = AUTHORITIES.get(
        authority_id
    )

    if authority is None:

        return {
            "matched": False,
            "issue_code": issue_code,
            "authority": None,
            "message": (
                "Issue code exists, but its authority "
                "mapping is unavailable."
            )
        }

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    return {
        "matched": True,
        "issue_code": issue_code,
        "authority": {
            "id": authority_id,
            **authority
        },
        "message": (
            "Authority resolved using the application's "
            "canonical issue mapping."
        )
    }