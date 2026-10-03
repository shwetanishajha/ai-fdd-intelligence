from pydantic import BaseModel,field_validator,Field
from typing import Literal


class FDDFinding(BaseModel):
    finding: str
    risk_level: str
    evidence: str
    source: str
    page: int
    confidence: float = Field(..., ge=0, le=1)   
    human_review_status: Literal["Pending", "Approved", "Rejected", "Amended"] = "Pending"
   
    @field_validator("risk_level")
    @classmethod
    def normalise_risk_level(cls, value: str) -> str:
        value = value.capitalize()

        if value not in {"Low", "Medium", "High"}:
            raise ValueError("risk_level must be Low, Medium, or High")

        return value