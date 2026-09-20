import pandas as pd


REGIME_FEATURE_COLUMNS = [
    "taiex_ret_5d",
    "taiex_ret_20d",
    "taiex_vol_20d",

    "spy_ret_5d",
    "spy_ret_20d",
    "qqq_ret_5d",
    "qqq_ret_20d",
    "soxx_ret_5d",
    "soxx_ret_20d",

    "tlt_ret_5d",
    "tlt_ret_20d",

    "usd_twd_ret_5d",
    "usd_twd_ret_20d",

    "vixy_ret_5d",
    "vixy_ret_20d",
]


class RegimeFeatureService:

    def align_market_data(
        self,
        taiex: pd.DataFrame,
        institutional: pd.DataFrame,
        usd_twd: pd.DataFrame,
        us_market: pd.DataFrame,
    ) -> pd.DataFrame:

        # =================================================
        # 1. Taiwan features
        # =================================================

        panel = (
            taiex
            .sort_values("date")
            .copy()
        )

        panel["taiex_ret_5d"] = (
            panel["taiex"].pct_change(5) * 100
        )

        panel["taiex_ret_20d"] = (
            panel["taiex"].pct_change(20) * 100
        )

        daily_ret = panel["taiex"].pct_change()

        panel["taiex_vol_20d"] = (
            daily_ret
            .rolling(20)
            .std()
            * (252 ** 0.5)
            * 100
        )

        # =================================================
        # 2. FX features
        # Calculate on FX's own observation calendar first
        # =================================================

        fx = (
            usd_twd
            .sort_values("date")
            .copy()
        )

        fx["usd_twd_ret_5d"] = (
            fx["usd_twd"].pct_change(5) * 100
        )

        fx["usd_twd_ret_20d"] = (
            fx["usd_twd"].pct_change(20) * 100
        )

        fx = fx[
            [
                "date",
                "usd_twd_ret_5d",
                "usd_twd_ret_20d",
            ]
        ]

        panel = pd.merge_asof(
            panel,
            fx,
            on="date",
            direction="backward",
            allow_exact_matches=True,
        )

        # =================================================
        # 3. US features
        # Calculate on US trading calendar BEFORE alignment
        # =================================================

        us = (
            us_market
            .sort_values("date")
            .copy()
        )

        for asset in [
            "spy",
            "qqq",
            "soxx",
            "tlt",
            "vixy",
        ]:
            us[f"{asset}_ret_5d"] = (
                us[asset].pct_change(5) * 100
            )

            us[f"{asset}_ret_20d"] = (
                us[asset].pct_change(20) * 100
            )

        us_feature_columns = [
            "date",

            "spy_ret_5d",
            "spy_ret_20d",

            "qqq_ret_5d",
            "qqq_ret_20d",

            "soxx_ret_5d",
            "soxx_ret_20d",

            "tlt_ret_5d",
            "tlt_ret_20d",

            "vixy_ret_5d",
            "vixy_ret_20d",
        ]

        us = us[us_feature_columns]

        # Taiwan date t can only use US data strictly before t.
        panel = pd.merge_asof(
            panel,
            us,
            on="date",
            direction="backward",
            allow_exact_matches=False,
        )

        return panel

    def add_price_features(
        self,
        panel: pd.DataFrame,
    ) -> pd.DataFrame:

        # Features are already calculated on each market's
        # native observation calendar before alignment.
        return (
            panel
            .sort_values("date")
            .reset_index(drop=True)
        )