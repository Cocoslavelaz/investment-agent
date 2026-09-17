from langchain_core.prompts import ChatPromptTemplate

from investment_agents.llm.factory import create_llm
from investment_agents.prompts.quantitative import (
    QUANTITATIVE_SYSTEM_PROMPT,
    QUANTITATIVE_FINE_GRAINED_PROMPT,
)
from investment_agents.schemas.agent_outputs import QuantitativeReport


class QuantitativeAgent:
    def __init__(self):
        llm = create_llm()

        self.llm = llm.with_structured_output(
            QuantitativeReport
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", QUANTITATIVE_SYSTEM_PROMPT),
                ("human", QUANTITATIVE_FINE_GRAINED_PROMPT),
            ]
        )

        self.chain = self.prompt | self.llm

    def analyze(self, metrics: dict) -> QuantitativeReport:
        return self.chain.invoke(metrics)