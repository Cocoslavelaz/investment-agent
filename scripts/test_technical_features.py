from investment_agents.data.clients.finmind import FinMindClient
from investment_agents.data.repositories.price import PriceRepository
from investment_agents.data.repositories.dividend import DividendRepository
from investment_agents.features.price_adjustment import PriceAdjustmentService
from investment_agents.features.technical import TechnicalFeatureService


client = FinMindClient()

price_repo = PriceRepository(client)
dividend_repo = DividendRepository(client)

adjustment_service = PriceAdjustmentService()
technical_service = TechnicalFeatureService()


# 12-month RoC 需要至少 252 個交易日
# 多抓一些作為 warm-up buffer
price_df = price_repo.get_history(
    ticker="2330",
    start_date="2023-10-01",
    end_date="2025-03-31",
)

dividend_df = dividend_repo.get_history(
    ticker="2330",
    start_date="2023-10-01",
    end_date="2025-03-31",
)

adjusted_df = adjustment_service.transform(
    price_df=price_df,
    dividend_df=dividend_df,
)

feature_df = technical_service.transform(
    adjusted_df
)

columns = [
    "date",
    "adj_close",
    "roc_5d",
    "roc_10d",
    "roc_20d",
    "roc_1m",
    "roc_3m",
    "roc_6m",
    "roc_12m",
    "bollinger_z",
    "rsi",
    "macd",
    "macd_signal",
    "macd_hist",
    "stochastic_k",
    "stochastic_d",
    "stochastic_j",
]

print(feature_df[columns].tail())
last = feature_df.iloc[-1]

print(last[[
    "date",
    "adj_close",
    "roc_5d",
    "roc_10d",
    "roc_20d",
    "roc_1m",
    "roc_3m",
    "roc_6m",
    "roc_12m",
    "bollinger_z",
    "rsi",
    "macd",
    "macd_signal",
    "macd_hist",
    "stochastic_k",
    "stochastic_d",
    "stochastic_j",
]])

print("\nNaN:")
print(last.isna())