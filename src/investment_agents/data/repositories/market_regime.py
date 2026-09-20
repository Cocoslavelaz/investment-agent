import pandas as pd


class MarketRegimeRepository:

    def __init__(self, client):
        self.client = client

    def get_data(
        self,
        start_date: str,
        end_date: str | None = None,
    ) -> dict[str, pd.DataFrame]:

        taiex, institutional, usd, us_market = (
            self.client.get_macro_indicators(
                start_date=start_date,
                end_date=end_date,
            )
        )

        return {
            "taiex": self._normalize_taiex(taiex),
            "institutional": self._normalize_institutional(institutional),
            "usd_twd": self._normalize_usd_twd(usd),
            "us_market": self._normalize_us_market(us_market),
        }

    @staticmethod
    def _normalize_taiex(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if df.empty:
            return pd.DataFrame(columns=["date", "taiex"])

        df["date"] = pd.to_datetime(df["date"])

        df = df.rename(columns={
            "price": "taiex",
        })

        df = (
            df[["date", "taiex"]]
            .drop_duplicates(subset=["date"])
            .sort_values("date")
            .reset_index(drop=True)
        )

        return df

    @staticmethod
    def _normalize_institutional(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if df.empty:
            return pd.DataFrame(
                columns=["date", "investor_type", "buy", "sell", "net_buy"]
            )

        df["date"] = pd.to_datetime(df["date"])

        df = df.rename(columns={
            "name": "investor_type",
        })

        # "total" 是 FinMind 已經加總的資料，
        # 保留會和各法人資料重複計算，因此先移除。
        df = df[df["investor_type"] != "total"].copy()

        df["net_buy"] = df["buy"] - df["sell"]

        df = (
            df[
                [
                    "date",
                    "investor_type",
                    "buy",
                    "sell",
                    "net_buy",
                ]
            ]
            .drop_duplicates(
                subset=["date", "investor_type"]
            )
            .sort_values(["date", "investor_type"])
            .reset_index(drop=True)
        )

        return df

    @staticmethod
    def _normalize_usd_twd(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if df.empty:
            return pd.DataFrame(
                columns=["date", "usd_twd"]
            )

        df["date"] = pd.to_datetime(df["date"])

        # 使用即期買賣中價，而不是現金匯率
        df["usd_twd"] = (
            df["spot_buy"] + df["spot_sell"]
        ) / 2

        df = (
            df[["date", "usd_twd"]]
            .drop_duplicates(subset=["date"])
            .sort_values("date")
            .reset_index(drop=True)
        )

        return df

    @staticmethod
    def _normalize_us_market(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if df.empty:
            return df

        df["date"] = pd.to_datetime(df["date"])

        # Regime 第一版只需要 adjusted close
        keep_columns = [
            "date",
            "SPY_Adj_Close",
            "QQQ_Adj_Close",
            "SOXX_Adj_Close",
            "TLT_Adj_Close",
            "UUP_Adj_Close",
            "VIXY_Adj_Close",
        ]

        df = df[keep_columns].rename(
            columns={
                "SPY_Adj_Close": "spy",
                "QQQ_Adj_Close": "qqq",
                "SOXX_Adj_Close": "soxx",
                "TLT_Adj_Close": "tlt",
                "UUP_Adj_Close": "uup",
                "VIXY_Adj_Close": "vixy",
            }
        )

        df = (
            df.drop_duplicates(subset=["date"])
            .sort_values("date")
            .reset_index(drop=True)
        )

        return df