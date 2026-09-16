from investment_agents.data.clients.finmind import FinMindClient
from investment_agents.data.repositories.price import PriceRepository
from investment_agents.data.repositories.dividend import DividendRepository
from investment_agents.features.price_adjustment import PriceAdjustmentService
from investment_agents.features.technical import TechnicalFeatureService
from investment_agents.snapshots.technical import TechnicalSnapshotService

# 這裡換成你目前 TechnicalAgent 的實際 import path
from investment_agents.agents.technical import TechnicalAgent


client = FinMindClient()

snapshot_service = TechnicalSnapshotService(
    price_repo=PriceRepository(client),
    dividend_repo=DividendRepository(client),
    adjustment_service=PriceAdjustmentService(),
    technical_service=TechnicalFeatureService(),
)

snapshot = snapshot_service.get_snapshot(
    ticker="2330",
    as_of_date="2025-03-31",
)

print("=== Technical Snapshot ===")

for key, value in snapshot.items():
    print(f"{key:20s}: {value:.4f}")


agent = TechnicalAgent()

report = agent.analyze(snapshot)

print("\n=== Technical Report ===")
print(report)