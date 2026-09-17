from langchain_core.prompts import ChatPromptTemplate

from investment_agents.llm.factory import create_llm
from investment_agents.prompts.sector import (
    SECTOR_SYSTEM_PROMPT,
    SECTOR_ANALYSIS_PROMPT,
)
from investment_agents.schemas.agent_outputs import SectorReport


class SectorAgent:
    def __init__(self):
        llm = create_llm()

        self.llm = llm.with_structured_output(
            SectorReport
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SECTOR_SYSTEM_PROMPT),
                ("human", SECTOR_ANALYSIS_PROMPT),
            ]
        )

        self.chain = self.prompt | self.llm

    def analyze(self, analysis_data: dict) -> SectorReport:
        return self.chain.invoke(analysis_data)