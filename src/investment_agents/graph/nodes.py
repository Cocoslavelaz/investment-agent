from investment_agents.agents.technical import TechnicalAgent
from investment_agents.agents.chip import ChipAgent
from investment_agents.agents.regime import MarketRegimeAgent
from investment_agents.agents.portfolio_manager import PortfolioManagerAgent

from investment_agents.schemas.state import InvestmentState


# ============================================================
# Agent instances
# ============================================================

technical_agent = TechnicalAgent()
chip_agent = ChipAgent()
regime_agent = MarketRegimeAgent()
pm_agent = PortfolioManagerAgent()


# ============================================================
# Technical Node
# ============================================================

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


# ============================================================
# Chip Node
# ============================================================

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


# ============================================================
# Market Regime Node
# ============================================================

def regime_node(state: InvestmentState) -> dict:
    print("[Regime Node] Running...")

    report = regime_agent.analyze(
        state["regime_data"]
    )

    print(
        "[Regime Node] Completed: "
        f"regime={report.regime}, "
        f"risk_score={report.risk_score}, "
        f"confidence={report.confidence}"
    )

    return {
        "regime_report": report
    }


# ============================================================
# Portfolio Manager Node
# ============================================================

def pm_node(state: InvestmentState) -> dict:
    print("[PM Node] Running...")

    technical = state["technical_report"]
    chip = state["chip_report"]
    regime = state["regime_report"]

    analysis_data = {
        # Stock identity
        "ticker": state["ticker"],
        "company_name": state["company_name"],

        # Stock-level alpha signals
        "technical_score": technical.score,
        "technical_reason": technical.reason,

        "chip_score": chip.score,
        "chip_reason": chip.reason,

        # Market-level risk environment
        "market_regime": regime.regime,
        "regime_risk_score": regime.risk_score,
        "regime_confidence": regime.confidence,
        "regime_summary": regime.summary,
    }

    report = pm_agent.analyze(
        analysis_data
    )

    print(
        "[PM Node] Completed: "
        f"final_score={report.final_score}, "
        f"conviction={report.conviction}"
    )

    return {
        "pm_report": report
    }