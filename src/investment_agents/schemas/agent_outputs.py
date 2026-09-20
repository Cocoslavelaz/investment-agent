from pydantic import BaseModel, Field
from typing import Literal


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

class QuantitativeReport(BaseModel):
    score: int = Field(
        ge=0,
        le=100,
        description=(
            "Quantitative fundamental attractiveness score. "
            "100 = Strong Long, 50 = Neutral, 0 = Strong Short."
        ),
    )
    reason: str = Field(
        description="A brief one-sentence rationale for the score."
    )

class MacroReport(BaseModel):
    market_direction: int = Field(
        ge=0,
        le=100,
        description=(
            "Expected equity market direction. "
            "0 = strongly bearish, 50 = neutral, 100 = strongly bullish."
        ),
    )

    risk_sentiment: int = Field(
        ge=0,
        le=100,
        description=(
            "Market risk sentiment. "
            "0 = extreme risk-off, 50 = neutral, 100 = strong risk-on."
        ),
    )

    economic_growth: int = Field(
        ge=0,
        le=100,
        description=(
            "Economic growth environment. "
            "0 = severe contraction, 50 = neutral, 100 = strong expansion."
        ),
    )

    interest_rates: int = Field(
        ge=0,
        le=100,
        description=(
            "Interest-rate environment from an equity-market perspective. "
            "0 = strongly unfavorable, 50 = neutral, 100 = strongly favorable."
        ),
    )

    inflation: int = Field(
        ge=0,
        le=100,
        description=(
            "Inflation environment from an equity-market perspective. "
            "0 = strongly unfavorable, 50 = neutral, 100 = strongly favorable."
        ),
    )

    summary: str = Field(
        description="Concise summary of the macroeconomic environment."
    )

class SectorReport(BaseModel):
    score: int = Field(
        ge=0,
        le=100,
        description=(
            "Overall stock attractiveness score after integrating "
            "specialist analyses and sector context. "
            "100 = Strong Long, 50 = Neutral, 0 = Strong Short."
        ),
    )

    investment_thesis: str = Field(
        description=(
            "Concise investment thesis explaining the integrated "
            "assessment and the most important supporting or conflicting signals."
        )
    )

class PMReport(BaseModel):
    final_score: int = Field(
        ge=0,
        le=100,
        description=(
            "Conditional investment attractiveness of the stock "
            "over the next several trading days to approximately "
            "one month."
        ),
    )

    conviction: int = Field(
        ge=0,
        le=100,
        description=(
            "Confidence in the final assessment based on the "
            "consistency and strength of the provided evidence."
        ),
    )

    reason: str = Field(
        description=(
            "Concise explanation of how Technical, Chip, and "
            "Market Regime evidence were integrated."
        ),
    )

class ChipReport(BaseModel):
    score: int = Field(
        ge=0,
        le=100,
        description="Institutional chip-flow attractiveness score.",
    )

    reason: str = Field(
        description="Concise explanation of institutional flow signals."
    )

class SectorReport(BaseModel):
    score: int
    investment_thesis: str




class MarketRegimeReport(BaseModel):
    regime: Literal[
        "strong_risk_on",
        "risk_on",
        "neutral",
        "risk_off",
        "strong_risk_off",
    ] = Field(
        description="Overall market risk regime."
    )

    risk_score: int = Field(
        ge=0,
        le=100,
        description=(
            "Overall favorability of the market environment for taking "
            "equity risk. 0 = strongly risk-off, 50 = neutral, "
            "100 = strongly risk-on."
        ),
    )

    confidence: int = Field(
        ge=0,
        le=100,
        description=(
            "Confidence in the regime assessment based on consistency "
            "of the provided market signals."
        ),
    )

    summary: str = Field(
        description="Concise explanation of the current market regime."
    )