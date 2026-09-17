import pandas as pd

class PriceAdjustmentService:

    def transform(
        self,
        price_df: pd.DataFrame,
        dividend_df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = price_df.copy()

        # 保證時間順序
        df = (
            df.sort_values("date")
            .reset_index(drop=True)
        )

        # --------------------------------------------------
        # 1. 沒有除權息事件
        # --------------------------------------------------
        if dividend_df.empty:
            df["adj_open"] = df["open"]
            df["adj_high"] = df["high"]
            df["adj_low"] = df["low"]
            df["adj_close"] = df["close"]

            return df

        # --------------------------------------------------
        # 2. 建立 corporate action adjustment factor
        # --------------------------------------------------
        events = dividend_df.copy()

        events = (
            events.sort_values("date")
            .reset_index(drop=True)
        )

        events["event_factor"] = (
            events["after_price"]
            / events["before_price"]
        )

        # --------------------------------------------------
        # 3. 每個交易日預設 adjustment factor = 1
        # --------------------------------------------------
        df["adjustment_factor"] = 1.0

        # --------------------------------------------------
        # 4. 每次 corporate action：
        #    只調整事件日「以前」的價格
        # --------------------------------------------------
        for row in events.itertuples(index=False):

            event_date = row.date
            event_factor = row.event_factor

            mask = df["date"] < event_date

            df.loc[
                mask,
                "adjustment_factor"
            ] *= event_factor

        # --------------------------------------------------
        # 5. Adjust OHLC
        # --------------------------------------------------
        df["adj_open"] = (
            df["open"]
            * df["adjustment_factor"]
        )

        df["adj_high"] = (
            df["high"]
            * df["adjustment_factor"]
        )

        df["adj_low"] = (
            df["low"]
            * df["adjustment_factor"]
        )

        df["adj_close"] = (
            df["close"]
            * df["adjustment_factor"]
        )

        return df