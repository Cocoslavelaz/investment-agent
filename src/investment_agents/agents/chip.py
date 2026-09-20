from langchain_core.prompts import ChatPromptTemplate

from investment_agents.llm.factory import create_llm
from investment_agents.prompts.chip import (
    CHIP_SYSTEM_PROMPT,
    CHIP_ANALYSIS_PROMPT,
)
from investment_agents.schemas.agent_outputs import ChipReport


class ChipAgent:
    def __init__(self):
        llm = create_llm()

        self.llm = llm.with_structured_output(
            ChipReport
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", CHIP_SYSTEM_PROMPT),
                ("human", CHIP_ANALYSIS_PROMPT),
            ]
        )

        self.chain = self.prompt | self.llm

    def analyze(
        self,
        indicators: dict,
    ) -> ChipReport:

        return self.chain.invoke(indicators)