from investment_agents.agents.macro import MacroAgent


agent = MacroAgent()

macro_data = {
    # Interest Rates
    "us_fed_funds_rate": 4.5,
    "us_fed_funds_rate_change": -0.25,

    "us_10y_yield": 4.1,
    "us_10y_yield_change": -0.15,

    "domestic_policy_rate": 2.0,
    "domestic_policy_rate_change": 0.0,

    "domestic_10y_yield": 1.6,
    "domestic_10y_yield_change": -0.05,

    # Inflation / Commodities
    "us_cpi": 2.8,
    "us_cpi_change": -0.2,

    "domestic_cpi": 2.1,
    "domestic_cpi_change": -0.1,

    "gold": 2350,
    "gold_change": 2.5,

    "crude_oil": 75,
    "crude_oil_change": -3.0,

    # Economic Growth
    "us_nonfarm_payrolls": 180_000,
    "us_nonfarm_payrolls_change": -20_000,

    "us_industrial_production": 1.2,
    "us_industrial_production_change": 0.1,

    "us_housing_starts": 1_450_000,
    "us_housing_starts_change": 20_000,

    "us_unemployment_rate": 4.0,
    "us_unemployment_rate_change": 0.1,

    "domestic_business_conditions": 102.5,
    "domestic_business_conditions_change": 0.8,

    # Market / Risk
    "usd_domestic_fx": 32.5,
    "usd_domestic_fx_change": -0.5,

    "domestic_stock_index": 22_500,
    "domestic_stock_index_change": 4.2,

    "sp500": 5_600,
    "sp500_change": 3.1,

    "vix": 14.5,
    "vix_change": -2.0,

    "domestic_volatility_index": 18.0,
    "domestic_volatility_index_change": -1.5,
}


result = agent.analyze(macro_data)

print(result)

print("Market Direction:", result.market_direction)
print("Risk Sentiment:", result.risk_sentiment)
print("Economic Growth:", result.economic_growth)
print("Interest Rates:", result.interest_rates)
print("Inflation:", result.inflation)
print("Summary:", result.summary)