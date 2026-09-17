from langchain_core.prompts import ChatPromptTemplate

from investment_agents.llm.factory import create_llm
from investment_agents.prompts.pm import (
    PM_SYSTEM_PROMPT,
    PM_ANALYSIS_PROMPT,
)
from investment_agents.schemas.agent_outputs import PMReport


class PortfolioManagerAgent:
    def __init__(self):
        llm = create_llm()

        self.llm = llm.with_structured_output(
            PMReport
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", PM_SYSTEM_PROMPT),
                ("human", PM_ANALYSIS_PROMPT),
            ]
        )

        self.chain = self.prompt | self.llm

    def analyze(self, analysis_data: dict) -> PMReport:
        return self.chain.invoke(analysis_data)