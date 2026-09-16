from investment_agents.data.clients.finmind import FinMindClient
from investment_agents.data.repositories.price import PriceRepository


client = FinMindClient()

repo = PriceRepository(
    client=client,
)

df = repo.get_history(
    ticker="2330",
    start_date="2025-01-01",
    end_date="2025-03-31",
)

print(df.head())
print(df.tail())
print(df.columns)
print(df.dtypes)