from investment_agents.llm.factory import create_llm
from investment_agents.schemas.agent_outputs import ChipReport


class ChipAgent:

    def __init__(self):
        llm = create_llm()

        self.llm = llm.with_structured_output(
            ChipReport
        )

    def analyze(
        self,
        indicators: dict,
    ) -> ChipReport:

        prompt = f"""
You are an institutional flow analyst specializing
in the Taiwan stock market.
Consider the magnitude, persistence, and consistency of
flows from each investor group.

Do not assume a fixed weight for any investor group.
Determine the relative importance of each group from the
observed flow magnitude and persistence.

Pay particular attention to divergence between investor
groups.

Evaluate the stock's institutional chip-flow
attractiveness from 0 to 100.

Interpretation:
- A positive flow ratio means net institutional buying.
- A negative flow ratio means net institutional selling.
- Flow ratio is net buy divided by total stock trading volume.
- buy_days_20d is the number of net-buying days during
  the latest 20 trading days.
- A positive streak means consecutive net-buying days.
- A negative streak means consecutive net-selling days.
- Investment Trust flows may provide important domestic
  institutional confirmation or divergence.
- Dealer_self should be treated as supplementary evidence.
- Do not mechanically average the indicators.
- Consider short-term flow, medium-term accumulation,
  persistence, and divergence between investor groups.

Foreign Investor:
- 1-day flow ratio: {indicators["foreign_flow_ratio_1d"]:.2f}%
- 5-day flow ratio: {indicators["foreign_flow_ratio_5d"]:.2f}%
- 20-day flow ratio: {indicators["foreign_flow_ratio_20d"]:.2f}%
- Buying days in last 20 days: {indicators["foreign_buy_days_20d"]:.0f}
- Current streak: {indicators["foreign_streak"]:.0f}

Investment Trust:
- 1-day flow ratio: {indicators["trust_flow_ratio_1d"]:.2f}%
- 5-day flow ratio: {indicators["trust_flow_ratio_5d"]:.2f}%
- 20-day flow ratio: {indicators["trust_flow_ratio_20d"]:.2f}%
- Buying days in last 20 days: {indicators["trust_buy_days_20d"]:.0f}
- Current streak: {indicators["trust_streak"]:.0f}

Dealer:
- 1-day flow ratio: {indicators["dealer_flow_ratio_1d"]:.2f}%
- 5-day flow ratio: {indicators["dealer_flow_ratio_5d"]:.2f}%
- 20-day flow ratio: {indicators["dealer_flow_ratio_20d"]:.2f}%
- Buying days in last 20 days: {indicators["dealer_buy_days_20d"]:.0f}
- Current streak: {indicators["dealer_streak"]:.0f}

Provide:
1. A score from 0 to 100, where a higher score means
   more attractive institutional chip-flow conditions.
2. A concise reason explaining the dominant institutional
   flow, persistence, and any important divergence.
"""

        return self.llm.invoke(prompt)