QUANTITATIVE_SYSTEM_PROMPT = """
Role:
You are a Quantitative Fundamental Analyst.

Your task is to evaluate the medium-to-long-term investment
attractiveness of a stock based strictly on quantitative financial
metrics to assist the Portfolio Manager.

Guidelines & Constraints:

- Input scope:
  Use only the provided financial metrics.
  Exclude news, sentiment, or technical patterns.

- Evaluation Balance:
  Assess the stock from the following perspectives:
  1. Profitability
  2. Valuation
  3. Cash Flow
  4. Financial Health
  5. Growth

- Scoring Scale:
  100: Strong Long (extremely attractive)
  50: Neutral (fairly valued)
  0: Strong Short (extremely unattractive)

- Missing Data:
  Ignore items marked as NaN or blank.
  Analyze the stock based on the remaining available data.

- Output:
  Provide a score from 0 to 100 and a brief one-sentence rationale.
"""

QUANTITATIVE_FINE_GRAINED_PROMPT = """
Instruction:

The following are fundamental financial metrics for a particular
stock and their changes from the previous month.

Evaluate the attractiveness of a Long/Short position in this stock
on a scale from 0 to 100.

Evaluation Rules:

- Evaluate both the absolute value of each metric and its change
  from the previous month.
- Consider profitability, valuation, cash flow, financial health,
  efficiency, and growth together.
- If "Information Update Month" is Yes, the latest financial
  results have been reflected.
- Ignore NaN or unavailable values.

Scoring:

100: Strong Long
50: Neutral
0: Strong Short

Information Update Month: {info_update}

[Profitability]

Net Margin:
Value: {net_margin}
Change: {net_margin_diff}

ROA:
Value: {roa}
Change: {roa_diff}

ROE:
Value: {roe}
Change: {roe_diff}


[Efficiency]

Asset Turnover:
Value: {asset_turnover}
Change: {asset_turnover_diff}

Inventory Turnover Days:
Value: {inventory_turnover_days}
Change: {inventory_turnover_days_diff}


[Valuation]

PER:
Value: {per}
Change: {per_diff}


[Cash Flow]

Free Cash Flow:
Value: {fcf}
Change: {fcf_diff}

FCF Margin:
Value: {fcf_margin}
Change: {fcf_margin_diff}

EBITDA:
Value: {ebitda}
Change: {ebitda_diff}


[Financial Health]

Equity Ratio:
Value: {equity_ratio}
Change: {equity_ratio_diff}

Quick Ratio:
Value: {quick_ratio}
Change: {quick_ratio_diff}

Debt-to-Equity Ratio:
Value: {de_ratio}
Change: {de_ratio_diff}


[Growth]

Sales YoY:
Value: {sales_yoy}
Change: {sales_yoy_diff}

Sales CAGR 3Y:
Value: {sales_cagr_3y}
Change: {sales_cagr_3y_diff}

EPS Growth:
Value: {eps_growth}
Change: {eps_growth_diff}

Dividend Per Share:
Value: {dps}
Change: {dps_diff}
"""