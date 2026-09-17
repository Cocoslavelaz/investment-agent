import pandas as pd


class InstitutionalRepository:

    def __init__(self, client):
        self.client = client

    def get_history(
        self,
        ticker: str,
        start_date: str,
        end_date: str | None = None,
    ) -> pd.DataFrame:

        df = self.client.get_institutional_investors(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )

        columns = [
            "date",
            "ticker",
            "investor_type",
            "buy",
            "sell",
            "net_buy",
        ]

        if df.empty:
            return pd.DataFrame(columns=columns)

        df = df.rename(
            columns={
                "stock_id": "ticker",
                "name": "investor_type",
            }
        )

        required = {
            "date",
            "ticker",
            "investor_type",
            "buy",
            "sell",
        }

        missing = required - set(df.columns)

        if missing:
            raise ValueError(
                f"Institutional data missing columns: {missing}"
            )

        df = df[
            [
                "date",
                "ticker",
                "investor_type",
                "buy",
                "sell",
            ]
        ].copy()

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
        )

        df["ticker"] = df["ticker"].astype(str)

        df["investor_type"] = (
            df["investor_type"]
            .astype(str)
        )

        for col in ["buy", "sell"]:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce",
            )

        df = df.dropna(
            subset=[
                "date",
                "ticker",
                "investor_type",
                "buy",
                "sell",
            ]
        )

        # 基礎衍生欄位，可以放 repository
        # 因為只是 buy - sell 的資料 normalization，
        # 還不是投資訊號工程。
        df["net_buy"] = (
            df["buy"]
            - df["sell"]
        )

        return (
            df
            .sort_values(
                ["date", "investor_type"]
            )
            .drop_duplicates(
                subset=[
                    "ticker",
                    "date",
                    "investor_type",
                ],
                keep="last",
            )
            .reset_index(drop=True)
        )