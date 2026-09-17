import numpy as np
import pandas as pd


class ChipFeatureService:

    INVESTOR_MAP = {
        "Foreign_Investor": "foreign",
        "Investment_Trust": "trust",
        "Dealer_self": "dealer",
    }

    def transform(
        self,
        institutional_df: pd.DataFrame,
        price_df: pd.DataFrame,
    ) -> pd.DataFrame:

        if institutional_df.empty:
            return pd.DataFrame()

        inst = institutional_df.copy()
        price = price_df.copy()

        inst = inst[
            inst["investor_type"].isin(self.INVESTOR_MAP)
        ].copy()

        inst["investor"] = (
            inst["investor_type"]
            .map(self.INVESTOR_MAP)
        )

        # --------------------------------------------------
        # 1. long format → wide format
        # --------------------------------------------------

        net_buy = (
            inst.pivot_table(
                index=["date", "ticker"],
                columns="investor",
                values="net_buy",
                aggfunc="sum",
            )
            .reset_index()
        )

        net_buy.columns.name = None

        # 某天某類法人沒有資料 → 視為 0
        for investor in self.INVESTOR_MAP.values():
            if investor not in net_buy.columns:
                net_buy[investor] = 0.0

        # --------------------------------------------------
        # 2. merge trading volume
        # --------------------------------------------------

        price = price[
            [
                "date",
                "ticker",
                "volume",
            ]
        ].copy()

        df = net_buy.merge(
            price,
            on=["date", "ticker"],
            how="left",
        )

        df = (
            df.sort_values("date")
            .reset_index(drop=True)
        )

        # --------------------------------------------------
        # 3. features by investor
        # --------------------------------------------------

        for investor in [
            "foreign",
            "trust",
            "dealer",
        ]:

            net = df[investor]

            # ---------- absolute flow ----------

            df[f"{investor}_net_buy_1d"] = net

            df[f"{investor}_net_buy_5d"] = (
                net.rolling(
                    5,
                    min_periods=5,
                ).sum()
            )

            df[f"{investor}_net_buy_20d"] = (
                net.rolling(
                    20,
                    min_periods=20,
                ).sum()
            )

            # ---------- volume normalized flow ----------

            df[f"{investor}_flow_ratio_1d"] = (
                net
                / df["volume"].replace(0, np.nan)
                * 100
            )

            df[f"{investor}_flow_ratio_5d"] = (
                net.rolling(5, min_periods=5).sum()
                / df["volume"]
                .rolling(5, min_periods=5)
                .sum()
                .replace(0, np.nan)
                * 100
            )

            df[f"{investor}_flow_ratio_20d"] = (
                net.rolling(20, min_periods=20).sum()
                / df["volume"]
                .rolling(20, min_periods=20)
                .sum()
                .replace(0, np.nan)
                * 100
            )

            # ---------- persistence ----------

            df[f"{investor}_buy_days_20d"] = (
                (net > 0)
                .astype(int)
                .rolling(
                    20,
                    min_periods=20,
                )
                .sum()
            )

            df[f"{investor}_streak"] = (
                self._calculate_streak(net)
            )

        return df

    @staticmethod
    def _calculate_streak(
        series: pd.Series,
    ) -> pd.Series:

        result = []
        streak = 0

        for value in series:

            if value > 0:

                if streak > 0:
                    streak += 1
                else:
                    streak = 1

            elif value < 0:

                if streak < 0:
                    streak -= 1
                else:
                    streak = -1

            else:
                streak = 0

            result.append(streak)

        return pd.Series(
            result,
            index=series.index,
            dtype=float,
        )