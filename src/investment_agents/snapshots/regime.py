from __future__ import annotations

import pandas as pd

from investment_agents.data.repositories.market_regime import (
    MarketRegimeRepository,
)
from investment_agents.features.regime import (
    RegimeFeatureService,
)


class MarketRegimeSnapshotService:
    """
    Build a point-in-time market regime snapshot for the Regime Agent.

    Flow:
        MarketRegimeRepository
            -> RegimeFeatureService
            -> select latest Taiwan trading day <= as_of_date
            -> validate features
            -> return agent-ready dict

    Notes
    -----
    - Taiwan trading dates are used as the master timeline.
    - US market data alignment must already be handled by
      RegimeFeatureService.align_market_data().
    - Same-calendar-date US close must NOT be used for a Taiwan
      decision on that date.
    """

    FEATURE_COLUMNS = [
        # Taiwan market
        "taiex_ret_5d",
        "taiex_ret_20d",
        "taiex_vol_20d",

        # US equity
        "spy_ret_5d",
        "spy_ret_20d",
        "qqq_ret_5d",
        "qqq_ret_20d",

        # Semiconductor environment
        "soxx_ret_5d",
        "soxx_ret_20d",

        # Treasury proxy
        "tlt_ret_5d",
        "tlt_ret_20d",

        # FX
        "usd_twd_ret_5d",
        "usd_twd_ret_20d",

        # Volatility proxy
        "vixy_ret_5d",
        "vixy_ret_20d",
    ]

    def __init__(
        self,
        repository: MarketRegimeRepository,
        feature_service: RegimeFeatureService | None = None,
        warmup_days: int = 120,
    ):
        self.repository = repository
        self.feature_service = (
            feature_service or RegimeFeatureService()
        )
        self.warmup_days = warmup_days

    def get_snapshot(
        self,
        as_of_date: str,
    ) -> dict[str, float]:
        """
        Return the latest available regime features as of `as_of_date`.

        Parameters
        ----------
        as_of_date:
            Decision date in YYYY-MM-DD format.

        Returns
        -------
        dict[str, float]
            Agent-ready regime feature dictionary.
        """

        as_of = pd.Timestamp(as_of_date)

        # --------------------------------------------------
        # 1. Determine warmup window
        # --------------------------------------------------

        start_date = (
            as_of - pd.Timedelta(days=self.warmup_days)
        ).strftime("%Y-%m-%d")

        end_date = as_of.strftime("%Y-%m-%d")

        # --------------------------------------------------
        # 2. Fetch normalized raw market data
        # --------------------------------------------------

        data = self.repository.get_data(
            start_date=start_date,
            end_date=end_date,
        )

        required_datasets = {
            "taiex",
            "institutional",
            "usd_twd",
            "us_market",
        }

        missing_datasets = (
            required_datasets - set(data.keys())
        )

        if missing_datasets:
            raise ValueError(
                "Missing regime datasets: "
                f"{sorted(missing_datasets)}"
            )

        # --------------------------------------------------
        # 3. Align point-in-time market data
        # --------------------------------------------------

        panel = self.feature_service.align_market_data(
            taiex=data["taiex"],
            institutional=data["institutional"],
            usd_twd=data["usd_twd"],
            us_market=data["us_market"],
        )

        if panel.empty:
            raise ValueError(
                f"No aligned market data available as of "
                f"{as_of_date}"
            )

        # --------------------------------------------------
        # 4. Generate regime features
        # --------------------------------------------------

        features = self.feature_service.add_price_features(
            panel
        )

        if features.empty:
            raise ValueError(
                f"No regime features available as of "
                f"{as_of_date}"
            )

        # --------------------------------------------------
        # 5. Only use information available <= as_of_date
        #
        # This also handles weekends / Taiwan holidays.
        # Example:
        # as_of_date = Sunday 2025-03-30
        # -> latest Taiwan row = Friday 2025-03-28
        # --------------------------------------------------

        available = features[
            features["date"] <= as_of
        ].copy()

        if available.empty:
            raise ValueError(
                f"No regime data available as of "
                f"{as_of_date}"
            )

        available = available.sort_values("date")

        latest = available.iloc[-1]

        # --------------------------------------------------
        # 6. Validate feature schema
        # --------------------------------------------------

        missing_columns = [
            col
            for col in self.FEATURE_COLUMNS
            if col not in features.columns
        ]

        if missing_columns:
            raise ValueError(
                "Missing regime feature columns: "
                f"{missing_columns}"
            )

        # --------------------------------------------------
        # 7. Validate NaN / infinite values
        # --------------------------------------------------

        feature_values = latest[
            self.FEATURE_COLUMNS
        ]

        missing_features = feature_values[
            feature_values.isna()
        ].index.tolist()

        if missing_features:
            data_date = pd.Timestamp(
                latest["date"]
            ).strftime("%Y-%m-%d")

            raise ValueError(
                f"Missing regime features on "
                f"{data_date}: "
                f"{missing_features}"
            )

        # --------------------------------------------------
        # 8. Build Agent input
        # --------------------------------------------------

        snapshot = {
            col: float(latest[col])
            for col in self.FEATURE_COLUMNS
        }

        return snapshot