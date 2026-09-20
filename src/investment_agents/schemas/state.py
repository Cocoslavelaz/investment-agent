from typing import TypedDict

from investment_agents.schemas.agent_outputs import (
    TechnicalReport,
    ChipReport,
    MarketRegimeReport,
    PMReport,
)


class InvestmentState(TypedDict, total=False):
    # Stock identity
    ticker: str
    company_name: str

    # Agent input data
    technical_data: dict
    chip_data: dict
    regime_data: dict

    # Agent outputs
    technical_report: TechnicalReport
    chip_report: ChipReport
    regime_report: MarketRegimeReport

    # Final PM output
    pm_report: PMReport