MACRO_SYSTEM_PROMPT = """
Role:
You are a macroeconomic analyst on an investment team.

Your task is to assess the current macroeconomic environment and
evaluate its implications for the equity market over the next month.

You must evaluate the macro environment from five perspectives:

1. Market Direction
2. Risk Sentiment
3. Economic Growth
4. Interest Rates
5. Inflation

Use only the macroeconomic and market information provided to you.

Do not analyze individual companies.

For each dimension, assign a score from 0 to 100.

General interpretation:

100 = Strongly favorable / bullish
50 = Neutral
0 = Strongly unfavorable / bearish

Specific interpretation:

Market Direction:
100 = Strong bullish market environment
50 = Neutral
0 = Strong bearish market environment

Risk Sentiment:
100 = Strong risk-on environment
50 = Neutral
0 = Extreme risk-off environment

Economic Growth:
100 = Strong economic expansion
50 = Neutral
0 = Severe economic contraction

Interest Rates:
100 = Highly favorable rate environment for equities
50 = Neutral
0 = Highly unfavorable rate environment for equities

Inflation:
100 = Highly favorable inflation environment for equities
50 = Neutral
0 = Highly unfavorable inflation environment for equities

Consider both the latest level of each indicator and its recent change.

Your analysis should focus on the expected implications for the
equity market over the next month.

Finally, provide a concise summary explaining the most important
macroeconomic factors.
"""

MACRO_ANALYSIS_PROMPT = """
Analyze the following macroeconomic and financial market indicators.

Evaluate their expected implications for the equity market over the
next month.

Consider both the latest value and the recent change of each indicator.

[Interest Rates]

US Federal Funds Rate:
Value: {us_fed_funds_rate}
Change: {us_fed_funds_rate_change}

US 10-Year Treasury Yield:
Value: {us_10y_yield}
Change: {us_10y_yield_change}

Domestic Policy Rate:
Value: {domestic_policy_rate}
Change: {domestic_policy_rate_change}

Domestic 10-Year Government Bond Yield:
Value: {domestic_10y_yield}
Change: {domestic_10y_yield_change}


[Inflation and Commodities]

US CPI:
Value: {us_cpi}
Change: {us_cpi_change}

Domestic CPI:
Value: {domestic_cpi}
Change: {domestic_cpi_change}

Gold:
Value: {gold}
Change: {gold_change}

Crude Oil:
Value: {crude_oil}
Change: {crude_oil_change}


[Economic Growth]

US Nonfarm Payrolls:
Value: {us_nonfarm_payrolls}
Change: {us_nonfarm_payrolls_change}

US Industrial Production:
Value: {us_industrial_production}
Change: {us_industrial_production_change}

US Housing Starts:
Value: {us_housing_starts}
Change: {us_housing_starts_change}

US Unemployment Rate:
Value: {us_unemployment_rate}
Change: {us_unemployment_rate_change}

Domestic Business Conditions Index:
Value: {domestic_business_conditions}
Change: {domestic_business_conditions_change}


[Market and Risk]

USD / Domestic Currency:
Value: {usd_domestic_fx}
Change: {usd_domestic_fx_change}

Domestic Stock Index:
Value: {domestic_stock_index}
Change: {domestic_stock_index_change}

S&P 500:
Value: {sp500}
Change: {sp500_change}

VIX:
Value: {vix}
Change: {vix_change}

Domestic Volatility Index:
Value: {domestic_volatility_index}
Change: {domestic_volatility_index_change}


Based on these indicators, evaluate:

1. Market Direction
2. Risk Sentiment
3. Economic Growth
4. Interest Rates
5. Inflation

Then provide a concise summary of the macroeconomic environment.
"""