from investment_agents.agents.technical import TechnicalAgent
# from investment_agents.agents.quantitative import QuantitativeAgent
from investment_agents.agents.macro import MacroAgent
from investment_agents.agents.sector import SectorAgent
from investment_agents.agents.portfolio_manager import PortfolioManagerAgent
from investment_agents.agents.chip import ChipAgent

from investment_agents.schemas.state import InvestmentState


technical_agent = TechnicalAgent()
# quantitative_agent = QuantitativeAgent()
chip_agent = ChipAgent()
macro_agent = MacroAgent()
sector_agent = SectorAgent()
pm_agent = PortfolioManagerAgent()

def technical_node(state: InvestmentState) -> dict:
    print("[Technical Node] Running...")

    report = technical_agent.analyze(
        state["technical_data"]
    )

    print(
        f"[Technical Node] Completed: score={report.score}"
    )

    return {
        "technical_report": report
    }

# def quantitative_node(state: InvestmentState) -> dict:
#     print("[Quantitative Node] Running...")

#     report = quantitative_agent.analyze(
#         state["quantitative_data"]
#     )

#     print(
#         f"[Quantitative Node] Completed: score={report.score}"
#     )

#     return {
#         "quantitative_report": report
#     }

def macro_node(state: InvestmentState) -> dict:
    print("[Macro Node] Running...")

    report = macro_agent.analyze(
        state["macro_data"]
    )

    print("[Macro Node] Completed")

    return {
        "macro_report": report
    }

def sector_node(state: InvestmentState) -> dict:
    print("[Sector Node] Running...")

    technical = state["technical_report"]
    chip = state["chip_report"]

    analysis_data = {
        "ticker": state["ticker"],
        "company_name": state["company_name"],
        "sector_name": state["sector_name"],

        "technical_score": technical.score,
        "technical_reason": technical.reason,

        "chip_score": chip.score,
        "chip_reason": chip.reason,

        "sector_context": state["sector_context"],
    }

    report = sector_agent.analyze(analysis_data)

    print(
        f"[Sector Node] Completed: score={report.score}"
    )

    return {
        "sector_report": report
    }

def pm_node(state: InvestmentState) -> dict:
    print("[PM Node] Running...")
    sector = state["sector_report"]
    macro = state["macro_report"]

    analysis_data = {
        "ticker": state["ticker"],
        "company_name": state["company_name"],
        "sector_name": state["sector_name"],

        "sector_score": sector.score,
        "sector_thesis": sector.investment_thesis,

        "market_direction": macro.market_direction,
        "risk_sentiment": macro.risk_sentiment,
        "economic_growth": macro.economic_growth,
        "interest_rates": macro.interest_rates,
        "inflation": macro.inflation,
        "macro_summary": macro.summary,
    }

    report = pm_agent.analyze(analysis_data)

    return {
        "pm_report": report
    }

def chip_node(state: InvestmentState) -> dict:
    print("[Chip Node] Running...")

    report = chip_agent.analyze(
        state["chip_data"]
    )

    print(
        f"[Chip Node] Completed: score={report.score}"
    )

    return {
        "chip_report": report
    }