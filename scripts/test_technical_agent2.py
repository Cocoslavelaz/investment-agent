from investment_agents.data.clients.finmind import FinMindClient
from investment_agents.data.repositories.price import PriceRepository
from investment_agents.data.repositories.dividend import DividendRepository

from investment_agents.features.price_adjustment import PriceAdjustmentService
from investment_agents.features.technical import TechnicalFeatureService

from investment_agents.snapshots.technical import TechnicalSnapshotService

from investment_agents.agents.technical import TechnicalAgent


def main():

    # =========================
    # Data Layer
    # =========================

    client = FinMindClient()

    price_repo = PriceRepository(client)
    dividend_repo = DividendRepository(client)

    # =========================
    # Feature Layer
    # =========================

    adjustment_service = PriceAdjustmentService()
    technical_service = TechnicalFeatureService()

    # =========================
    # Snapshot Layer
    # =========================

    snapshot_service = TechnicalSnapshotService(
        price_repo=price_repo,
        dividend_repo=dividend_repo,
        adjustment_service=adjustment_service,
        technical_service=technical_service,
    )

    snapshot = snapshot_service.get_snapshot(
        ticker="2330",
        as_of_date="2025-03-31",
    )

    print("=== Technical Snapshot ===")

    for key, value in snapshot.items():
        print(f"{key:20s}: {value:.4f}")

    # =========================
    # Agent Layer
    # =========================

    agent = TechnicalAgent()

    report = agent.analyze(snapshot)

    print("\n=== Technical Agent Report ===")
    print(f"Score : {report.score}")
    print(f"Reason: {report.reason}")


if __name__ == "__main__":
    main()