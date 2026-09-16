from investment_agents.graph.investment_graph import (
    build_investment_graph,
)


graph = build_investment_graph()


initial_state = {
    "ticker": "TEST",
    "company_name": "Test Semiconductor Corp.",
    "sector_name": "Semiconductors",

    "technical_data": {
        # 把之前 test_technical_agent.py
        # 的 indicators 貼進來
    },

    "quantitative_data": {
        # 把之前 test_quantitative_agent.py
        # 的 metrics 貼進來
    },

    "macro_data": {
        # 把之前 test_macro_agent.py
        # 的 macro_data 貼進來
    },

    "sector_context": """
    The semiconductor sector currently benefits from strong AI and
    high-performance computing demand, although valuations remain
    elevated relative to historical averages.
    """,

    "technical_report": None,
    "quantitative_report": None,
    "macro_report": None,
    "sector_report": None,
    "pm_report": None,
}


result = graph.invoke(initial_state)


print("\n=== Technical ===")
print(result["technical_report"])

print("\n=== Quantitative ===")
print(result["quantitative_report"])

print("\n=== Macro ===")
print(result["macro_report"])

print("\n=== Sector ===")
print(result["sector_report"])

print("\n=== Portfolio Manager ===")
print(result["pm_report"])

print(
    "\nFinal Score:",
    result["pm_report"].final_score,
)