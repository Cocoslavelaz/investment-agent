from investment_agents.agents.sector import SectorAgent


agent = SectorAgent()

analysis_data = {
    "ticker": "TEST",
    "company_name": "Test Semiconductor Corp.",
    "sector_name": "Semiconductors",

    # Technical is strongly bullish
    "technical_score": 88,
    "technical_reason": (
        "Strong positive momentum across short and medium-term "
        "timeframes, with bullish MACD and RSI remaining below "
        "extreme overbought levels."
    ),

    # Fundamentals are weak
    "quantitative_score": 42,
    "quantitative_reason": (
        "Profitability remains healthy, but valuation is expensive "
        "and earnings growth has slowed significantly."
    ),

    "sector_context": """
    The semiconductor sector has shown strong recent momentum,
    supported by demand for AI and high-performance computing.

    However, sector valuations are currently above their historical
    averages, and several companies are experiencing slower earnings growth.

    The target company has stronger profitability than the sector average,
    but also trades at a higher valuation multiple.
    """,
}


result = agent.analyze(analysis_data)

print(result)
print("Sector Score:", result.score)
print("Investment Thesis:", result.investment_thesis)