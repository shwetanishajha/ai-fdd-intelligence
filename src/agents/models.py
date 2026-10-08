from pydantic import BaseModel, field_validator, Field
from typing import Literal


class FindingProvenance(BaseModel):
    question: str
    agent: str
    source: str
    page: int
    generated_at: str


class FDDFinding(BaseModel):
    finding: str
    risk_level: str
    evidence: str
    source: str
    page: int
    confidence: float = Field(..., ge=0, le=1)

    human_review_status: Literal[
        "Pending",
        "Approved",
        "Rejected",
        "Amended",
    ] = "Pending"

    provenance: FindingProvenance | None = None

    @field_validator("risk_level")
    @classmethod
    def normalise_risk_level(cls, value: str) -> str:
        value = value.capitalize()

        if value not in {
            "Low",
            "Medium",
            "High",
        }:
            raise ValueError(
                "risk_level must be Low, Medium, or High"
            )

        return value


class KeyRisk(BaseModel):
    risk: str
    evidence: str | dict | list[dict]


class FDDReport(BaseModel):
    executive_summary: dict
    company_overview: dict
    revenue_analysis: dict
    ebitda_analysis: dict
    working_capital_analysis: dict
    customer_concentration: dict
    financial_anomalies: dict

    key_risks: list[KeyRisk] = Field(
        min_length=1
    )

    further_diligence: dict
    evidence_register: list[dict] = Field(
        min_length=1
    )