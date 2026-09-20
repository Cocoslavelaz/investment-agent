from langchain_core.prompts import ChatPromptTemplate

from investment_agents.llm.factory import create_llm
from investment_agents.schemas.agent_outputs import MarketRegimeReport
from investment_agents.prompts.regime import (
    REGIME_SYSTEM_PROMPT,
    REGIME_ANALYSIS_PROMPT,
)


class MarketRegimeAgent:

    def __init__(self):
        llm = create_llm()

        self.llm = llm.with_structured_output(
            MarketRegimeReport
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", REGIME_SYSTEM_PROMPT),
            ("human", REGIME_ANALYSIS_PROMPT),
        ])

        self.chain = self.prompt | self.llm

    def analyze(
        self,
        regime_data: dict,
    ) -> MarketRegimeReport:

        return self.chain.invoke(regime_data)