from langgraph.graph import StateGraph, START, END

from investment_agents.schemas.state import InvestmentState
from investment_agents.graph.nodes import (
    technical_node,
    quantitative_node,
    macro_node,
    sector_node,
    pm_node,
    chip_node
)


def build_investment_graph():
    builder = StateGraph(InvestmentState)

    builder.add_node("technical", technical_node)
    builder.add_node("chip", chip_node)
    builder.add_node("macro", macro_node)
    builder.add_node("sector", sector_node)
    builder.add_node("pm", pm_node)

    builder.add_edge(START, "technical")
    builder.add_edge(START, "chip")
    builder.add_edge(START, "macro")

    builder.add_edge(
        ["technical", "chip"],
        "sector",
    )

    builder.add_edge(
        ["sector", "macro"],
        "pm",
    )

    builder.add_edge("pm", END)

    return builder.compile()