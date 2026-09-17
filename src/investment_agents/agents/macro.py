from langchain_core.prompts import ChatPromptTemplate

from investment_agents.llm.factory import create_llm
from investment_agents.prompts.macro import (
    MACRO_SYSTEM_PROMPT,
    MACRO_ANALYSIS_PROMPT,
)
from investment_agents.schemas.agent_outputs import MacroReport


class MacroAgent:
    def __init__(self):
        llm = create_llm()

        self.llm = llm.with_structured_output(
            MacroReport
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", MACRO_SYSTEM_PROMPT),
                ("human", MACRO_ANALYSIS_PROMPT),
            ]
        )

        self.chain = self.prompt | self.llm

    def analyze(self, macro_data: dict) -> MacroReport:
        return self.chain.invoke(macro_data)