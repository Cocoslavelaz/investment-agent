import pandas as pd

from investment_agents.data.repositories.price import PriceRepository
from investment_agents.data.repositories.institutional import InstitutionalRepository
from investment_agents.features.chip import ChipFeatureService


class ChipSnapshotService:

    FEATURE_COLUMNS = [
        "foreign_flow_ratio_1d",
        "foreign_flow_ratio_5d",
        "foreign_flow_ratio_20d",
        "foreign_buy_days_20d",
        "foreign_streak",

        "trust_flow_ratio_1d",
        "trust_flow_ratio_5d",
        "trust_flow_ratio_20d",
        "trust_buy_days_20d",
        "trust_streak",

        "dealer_flow_ratio_1d",
        "dealer_flow_ratio_5d",
        "dealer_flow_ratio_20d",
        "dealer_buy_days_20d",
        "dealer_streak",
    ]

    def __init__(
        self,
        price_repo: PriceRepository,
        institutional_repo: InstitutionalRepository,
        chip_service: ChipFeatureService,
    ):
        self.price_repo = price_repo
        self.institutional_repo = institutional_repo
        self.chip_service = chip_service

    def get_snapshot(
        self,
        ticker: str,
        as_of_date: str,
    ) -> dict:

        as_of = pd.Timestamp(as_of_date)

        # 20 trading days + buffer
        start_date = (
            as_of - pd.Timedelta(days=60)
        )

        price_df = self.price_repo.get_history(
            ticker=ticker,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=as_of.strftime("%Y-%m-%d"),
        )

        institutional_df = (
            self.institutional_repo.get_history(
                ticker=ticker,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=as_of.strftime("%Y-%m-%d"),
            )
        )

        if price_df.empty:
            raise ValueError(
                f"No price data for {ticker} "
                f"as of {as_of_date}"
            )

        if institutional_df.empty:
            raise ValueError(
                f"No institutional data for {ticker} "
                f"as of {as_of_date}"
            )

        feature_df = self.chip_service.transform(
            institutional_df=institutional_df,
            price_df=price_df,
        )

        available_df = feature_df[
            feature_df["date"] <= as_of
        ]

        if available_df.empty:
            raise ValueError(
                f"No chip features for {ticker} "
                f"as of {as_of_date}"
            )

        latest = available_df.iloc[-1]

        missing = [
            col
            for col in self.FEATURE_COLUMNS
            if pd.isna(latest[col])
        ]

        if missing:
            raise ValueError(
                f"Chip features unavailable for "
                f"{ticker} as of {as_of_date}: {missing}"
            )

        return {
            col: float(latest[col])
            for col in self.FEATURE_COLUMNS
        }