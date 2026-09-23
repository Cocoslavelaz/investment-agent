from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
#論文保留 stochasticity，並透過多次 trial / aggregation 處理 variation

# def create_llm() -> ChatOpenAI:
#     return ChatOpenAI(
#         model="gpt-4o",
#         temperature=0.0,
#     )

def create_llm() -> ChatOllama:

    return ChatOllama(
        model="qwen3:14b",
        temperature=0.0,

        # Context window
        num_ctx=8192,

        # Maximum generated tokens.
        # Agent outputs only contain score/reason, so 512 is enough.
        num_predict=512,

        # Keep model loaded in VRAM/RAM between agent calls.
        keep_alive="30m",

        # Qwen3 supports thinking mode.
        # Disable it for high-throughput structured-output agents.
        reasoning=False,
    )