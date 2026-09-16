from investment_agents.agents.quantitative import QuantitativeAgent


agent = QuantitativeAgent()

metrics = {
    "info_update": "Yes",

    # Profitability
    "net_margin": 18.5,
    "net_margin_diff": 1.2,

    "roa": 12.3,
    "roa_diff": 0.8,

    "roe": 21.7,
    "roe_diff": 1.5,

    # Efficiency
    "asset_turnover": 0.85,
    "asset_turnover_diff": 0.03,

    "inventory_turnover_days": 42.0,
    "inventory_turnover_days_diff": -3.0,

    # Valuation
    "per": 16.2,
    "per_diff": -1.1,

    # Cash Flow
    "fcf": 125_000_000,
    "fcf_diff": 8_000_000,

    "fcf_margin": 14.2,
    "fcf_margin_diff": 0.9,

    "ebitda": 210_000_000,
    "ebitda_diff": 12_000_000,

    # Financial Health
    "equity_ratio": 62.0,
    "equity_ratio_diff": 1.0,

    "quick_ratio": 1.8,
    "quick_ratio_diff": 0.1,

    "de_ratio": 0.35,
    "de_ratio_diff": -0.04,

    # Growth
    "sales_yoy": 11.5,
    "sales_yoy_diff": 2.0,

    "sales_cagr_3y": 9.2,
    "sales_cagr_3y_diff": 0.5,

    "eps_growth": 15.8,
    "eps_growth_diff": 3.1,

    "dps": 5.0,
    "dps_diff": 0.5,
}

result = agent.analyze(metrics)

print(result)
print("Score:", result.score)
print("Reason:", result.reason)