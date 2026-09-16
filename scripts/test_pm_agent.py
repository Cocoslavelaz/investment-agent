from investment_agents.agents.portfolio_manager import (
    PortfolioManagerAgent,
)


agent = PortfolioManagerAgent()

analysis_data = {
    "ticker": "TEST",
    "company_name": "Test Semiconductor Corp.",
    "sector_name": "Semiconductors",

    # Bottom-up: positive
    "sector_score": 72,
    "sector_thesis": (
        "The company shows strong technical momentum and above-sector "
        "profitability, supported by structural AI demand. However, "
        "valuation remains elevated and earnings growth has moderated."
    ),

    # Top-down: intentionally weak
    "market_direction": 38,
    "risk_sentiment": 30,
    "economic_growth": 45,
    "interest_rates": 35,
    "inflation": 42,

    "macro_summary": (
        "The macro environment is moderately risk-off. Equity markets "
        "face pressure from restrictive financial conditions and weak "
        "risk appetite, while economic growth is slowing."
    ),
}


result = agent.analyze(analysis_data)

print(result)
print("Final Score:", result.final_score)
print("Reason:", result.reason)