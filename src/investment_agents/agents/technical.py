from investment_agents.llm.factory import create_llm
from investment_agents.schemas.agent_outputs import TechnicalReport


class TechnicalAgent:

    def __init__(self):
        llm = create_llm()

        self.llm = llm.with_structured_output(
            TechnicalReport
        )

    def analyze(
        self,
        indicators: dict,
    ) -> TechnicalReport:

        prompt = f"""
You are a technical analyst.

Evaluate the stock's technical attractiveness
based on the following indicators.

Momentum:
- 5-day RoC: {indicators["roc_5d"]:.2f}%
- 10-day RoC: {indicators["roc_10d"]:.2f}%
- 20-day RoC: {indicators["roc_20d"]:.2f}%
- 1-month RoC: {indicators["roc_1m"]:.2f}%
- 3-month RoC: {indicators["roc_3m"]:.2f}%
- 6-month RoC: {indicators["roc_6m"]:.2f}%
- 12-month RoC: {indicators["roc_12m"]:.2f}%

Bollinger:
- Z-score: {indicators["bollinger_z"]:.2f}

RSI:
- RSI: {indicators["rsi"]:.2f}

MACD:
- MACD: {indicators["macd"]:.2f}
- Signal: {indicators["macd_signal"]:.2f}
- Histogram: {indicators["macd_hist"]:.2f}

Stochastic:
- K: {indicators["stochastic_k"]:.2f}
- D: {indicators["stochastic_d"]:.2f}
- J: {indicators["stochastic_j"]:.2f}

Return:
- score: technical attractiveness from 0 to 100
- reason: concise explanation of the technical signals
"""

        return self.llm.invoke(prompt)