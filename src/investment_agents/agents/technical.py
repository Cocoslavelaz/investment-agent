from langchain_core.prompts import ChatPromptTemplate

from investment_agents.llm.factory import create_llm
from investment_agents.prompts.technical import (
    TECHNICAL_SYSTEM_PROMPT,
    TECHNICAL_FINE_GRAINED_PROMPT,
)
from investment_agents.schemas.agent_outputs import TechnicalReport


class TechnicalAgent:

    def __init__(self):
        llm = create_llm()

        self.llm = llm.with_structured_output(
            TechnicalReport
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", TECHNICAL_SYSTEM_PROMPT),
                ("human", TECHNICAL_FINE_GRAINED_PROMPT),
            ]
        )

        self.chain = self.prompt | self.llm

    def analyze(
        self,
        indicators: dict,
    ) -> TechnicalReport:

        return self.chain.invoke(indicators)