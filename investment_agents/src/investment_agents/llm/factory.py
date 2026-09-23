from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
#論文保留 stochasticity，並透過多次 trial / aggregation 處理 variation

def create_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-4o",
        temperature=1.0,
    )