from pydantic import BaseModel, Field
from typing import List


class SeverityAssessment(BaseModel):
    score: float = Field(
        ge=0,
        le=10,
        description="Civic risk score from 0 to 10"
    )

    level: str = Field(
        description="Minor, Moderate, Serious, or Critical"
    )

    urgency: str = Field(
        description="Low, Medium, High, or Immediate"
    )


class AuthorityRecommendation(BaseModel):
    authority_type: str
    department: str


class CivicIssueAnalysis(BaseModel):
    issue_code: str

    issue: str
    category: str

    severity: SeverityAssessment

    visible_evidence: List[str]
    potential_risks: List[str]

    recommended_authority: AuthorityRecommendation

    citizen_instructions: List[str]
    required_report_information: List[str]

    complaint_subject: str
    complaint_letter: str