from langgraph.graph import StateGraph, START, END

from investment_agents.schemas.state import InvestmentState
from investment_agents.graph.nodes import (
    technical_node,
    chip_node,
    regime_node,
    pm_node,
)


def build_investment_graph():
    builder = StateGraph(InvestmentState)

    # ==========================================
    # Nodes
    # ==========================================

    builder.add_node(
        "technical",
        technical_node,
    )

    builder.add_node(
        "chip",
        chip_node,
    )

    builder.add_node(
        "regime",
        regime_node,
    )

    builder.add_node(
        "pm",
        pm_node,
    )

    # ==========================================
    # Level 1:
    # Independent specialist agents
    # ==========================================

    builder.add_edge(
        START,
        "technical",
    )

    builder.add_edge(
        START,
        "chip",
    )

    builder.add_edge(
        START,
        "regime",
    )

    # ==========================================
    # Level 2:
    # Portfolio Manager
    #
    # PM waits until all three specialist
    # reports are available.
    # ==========================================

    builder.add_edge(
        [
            "technical",
            "chip",
            "regime",
        ],
        "pm",
    )

    # ==========================================
    # End
    # ==========================================

    builder.add_edge(
        "pm",
        END,
    )

    return builder.compile()