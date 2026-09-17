import pandas as pd

from investment_agents.data.clients.finmind import FinMindClient


class PriceRepository:

    def __init__(self, client: FinMindClient):
        self.client = client

    def get_history(
        self,
        ticker: str,
        start_date: str,
        end_date: str | None = None,
    ) -> pd.DataFrame:

        # 1. 取得 FinMind raw data
        df = self.client.get_stock_price(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )

        # 2. FinMind schema → internal schema
        rename_map = {
            "stock_id": "ticker",
            "Trading_Volume": "volume",
            "Trading_money": "trading_money",
            "Trading_turnover": "turnover",
            "max": "high",
            "min": "low",
        }

        df = df.rename(columns=rename_map)

        # 3. 我們 Price domain 需要的欄位
        columns = [
            "date",
            "ticker",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "trading_money",
            "turnover",
        ]

        df = df.rename(columns=rename_map)
        missing_cols = set(columns) - set(df.columns)

        if missing_cols:
            raise ValueError(
                f"Price data missing columns: {missing_cols}"
            )

        df = df[columns].copy()

        # 4. datatype normalization
        df["date"] = pd.to_datetime(df["date"])
        df["ticker"] = df["ticker"].astype(str)

        numeric_cols = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "trading_money",
            "turnover",
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce",
            )

        # 5. 排序 / 去重
        df = (
            df.sort_values("date")
            .drop_duplicates(
                subset=["ticker", "date"]
            )
            .reset_index(drop=True)
        )

        return df