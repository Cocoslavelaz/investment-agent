from investment_agents.data.clients.finmind import FinMindClient
from investment_agents.data.repositories.price import PriceRepository
from investment_agents.data.repositories.dividend import DividendRepository
from investment_agents.features.price_adjustment import PriceAdjustmentService


client = FinMindClient()

price_repo = PriceRepository(client)
dividend_repo = DividendRepository(client)

adjustment_service = PriceAdjustmentService()


price_df = price_repo.get_history(
    ticker="2330",
    start_date="2025-03-10",
    end_date="2025-03-25",
)

dividend_df = dividend_repo.get_history(
    ticker="2330",
    start_date="2025-03-10",
    end_date="2025-03-25",
)

adjusted_df = adjustment_service.transform(
    price_df=price_df,
    dividend_df=dividend_df,
)

adjusted_df["raw_return"] = (
    adjusted_df["close"]
    .pct_change()
)

adjusted_df["adjusted_return"] = (
    adjusted_df["adj_close"]
    .pct_change()
)

print(
    adjusted_df[
        [
            "date",
            "close",
            "adj_close",
            "raw_return",
            "adjusted_return",
        ]
    ]
)