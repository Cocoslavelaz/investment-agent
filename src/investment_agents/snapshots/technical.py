import pandas as pd

from investment_agents.data.repositories.price import PriceRepository
from investment_agents.data.repositories.dividend import DividendRepository
from investment_agents.features.price_adjustment import PriceAdjustmentService
from investment_agents.features.technical import TechnicalFeatureService


class TechnicalSnapshotService:

    def __init__(
        self,
        price_repo: PriceRepository,
        dividend_repo: DividendRepository,
        adjustment_service: PriceAdjustmentService,
        technical_service: TechnicalFeatureService,
    ):
        self.price_repo = price_repo
        self.dividend_repo = dividend_repo
        self.adjustment_service = adjustment_service
        self.technical_service = technical_service

    def get_snapshot(
        self,
        ticker: str,
        as_of_date: str,
    ) -> dict:

        as_of = pd.Timestamp(as_of_date)

        # 12-month RoC requires ~252 trading days.
        # Use a conservative calendar-day warm-up window.
        start_date = as_of - pd.Timedelta(days=450)

        price_df = self.price_repo.get_history(
            ticker=ticker,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=as_of.strftime("%Y-%m-%d"),
        )

        if price_df.empty:
            raise ValueError(
                f"No price data available for {ticker} "
                f"as of {as_of_date}"
            )

        dividend_df = self.dividend_repo.get_history(
            ticker=ticker,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=as_of.strftime("%Y-%m-%d"),
        )

        adjusted_df = self.adjustment_service.transform(
            price_df=price_df,
            dividend_df=dividend_df,
        )

        feature_df = self.technical_service.transform(
            adjusted_df
        )

        # Point-in-time protection
        available_df = feature_df[
            feature_df["date"] <= as_of
        ]

        if available_df.empty:
            raise ValueError(
                f"No technical data available for {ticker} "
                f"as of {as_of_date}"
            )

        latest = available_df.iloc[-1]

        feature_columns = [
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

        missing_features = [
            col
            for col in feature_columns
            if pd.isna(latest[col])
        ]

        if missing_features:
            raise ValueError(
                f"Technical features unavailable for {ticker} "
                f"as of {as_of_date}: {missing_features}"
            )

        snapshot = {
            col: float(latest[col])
            for col in feature_columns
        }

        return snapshot