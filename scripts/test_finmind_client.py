from investment_agents.data.clients.finmind import FinMindClient
from investment_agents.data.repositories.dividend import DividendRepository

client = FinMindClient()

# df = client.get_stock_price(
#     ticker="2330",
#     start_date="2025-01-01",
#     end_date="2025-03-31",
# )

repo = DividendRepository(
    client=client,
)

df = repo.get_history(
    ticker="2330",
    start_date="2024-01-01",
    end_date="2025-03-31",
)

print(df)
print(df.columns)
print(df.dtypes)
