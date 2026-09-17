import pandas as pd 
from investment_agents.data.clients.finmind import FinMindClient

class DividendRepository:

    def __init__(self, client):
        self.client = client

    def get_history(
        self,
        ticker: str,
        start_date: str,
        end_date: str | None = None,
    ) -> pd.DataFrame:

        df = self.client.get_stock_dividend(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )

        columns = [
            "date",
            "ticker",
            "before_price",
            "after_price",
        ]

        # 沒有除權息資料是合法狀態
        if df.empty:
            return pd.DataFrame(columns=columns)

        rename_map = {
            "stock_id": "ticker",
        }

        df = df.rename(columns=rename_map)

        missing_cols = set(columns) - set(df.columns)

        if missing_cols:
            raise ValueError(
                f"Dividend data missing columns: {missing_cols}"
            )

        df = df[columns].copy()

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
        )

        df["ticker"] = df["ticker"].astype(str)

        numeric_cols = [
            "before_price",
            "after_price",
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce",
            )

        df = df.dropna(
            subset=[
                "date",
                "ticker",
                "before_price",
                "after_price",
            ]
        )

        df = df[
            (df["before_price"] > 0)
            & (df["after_price"] > 0)
        ]

        return (
            df.sort_values("date")
            .drop_duplicates(
                subset=["ticker", "date"],
                keep="last",
            )
            .reset_index(drop=True)
        )