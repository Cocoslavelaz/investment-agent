from investment_agents.data.clients.finmind import FinMindClient
from investment_agents.data.repositories.price import PriceRepository
from investment_agents.data.repositories.dividend import DividendRepository
from investment_agents.features.price_adjustment import PriceAdjustmentService
from investment_agents.features.technical import TechnicalFeatureService
from investment_agents.snapshots.technical import TechnicalSnapshotService


client = FinMindClient()

price_repo = PriceRepository(client)
dividend_repo = DividendRepository(client)

adjustment_service = PriceAdjustmentService()
technical_service = TechnicalFeatureService()

snapshot_service = TechnicalSnapshotService(
    price_repo=price_repo,
    dividend_repo=dividend_repo,
    adjustment_service=adjustment_service,
    technical_service=technical_service,
)


snapshot = snapshot_service.get_snapshot(
    ticker="2330",
    as_of_date="2025-03-30",
)

for key, value in snapshot.items():
    print(f"{key:20s}: {value:.4f}")