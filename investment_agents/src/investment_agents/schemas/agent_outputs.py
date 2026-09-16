from pydantic import BaseModel, Field


class TechnicalReport(BaseModel):
    score: int = Field(
        ge=0,
        le=100,
        description=(
            "Technical attractiveness score. "
            "100 = Strong Long, 50 = Neutral, 0 = Strong Short."
        ),
    )

    reason: str = Field(
        description="A brief one-sentence rationale for the score."
    )