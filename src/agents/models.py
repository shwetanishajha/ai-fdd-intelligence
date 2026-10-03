from pydantic import BaseModel
from typing import Literal


class FDDFinding(BaseModel):
    finding: str
    risk_level: Literal["Low", "Medium", "High"]
    evidence: str
    source: str
    page: int
    human_review_status: Literal["Pending", "Approved", "Rejected", "Amended"] = "Pending"