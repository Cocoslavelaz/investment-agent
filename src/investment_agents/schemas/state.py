from typing import TypedDict

from investment_agents.schemas.agent_outputs import (
    TechnicalReport,
    QuantitativeReport,
    MacroReport,
    SectorReport,
    PMReport,
    ChipReport
)


class InvestmentState(TypedDict, total=False):
    ticker: str
    company_name: str
    sector_name: str

    technical_data: dict
    chip_data: dict
    macro_data: dict
    sector_context: dict

    technical_report: TechnicalReport
    chip_report: ChipReport
    macro_report: MacroReport
    sector_report: SectorReport
    pm_report: PMReport