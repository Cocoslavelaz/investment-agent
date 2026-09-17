import numpy as np
import pandas as pd
import talib


class TechnicalFeatureService:

    def transform(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        # 確保時間順序正確
        df = (
            df.sort_values("date")
            .reset_index(drop=True)
        )

        self._validate(df)

        # Momentum
        df = self._add_roc(df)

        # Volatility
        df = self._add_bollinger_z(df)

        # Oscillators / Trend
        df = self._add_rsi(df)
        df = self._add_macd(df)
        df = self._add_stochastic(df)

        return df

    @staticmethod
    def _validate(df: pd.DataFrame) -> None:

        required_columns = {
            "date",
            "adj_open",
            "adj_high",
            "adj_low",
            "adj_close",
        }

        missing = required_columns - set(df.columns)

        if missing:
            raise ValueError(
                f"Technical feature input missing columns: {missing}"
            )

    @staticmethod
    def _add_roc(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        price = df["adj_close"]

        periods = {
            "roc_5d": 5,
            "roc_10d": 10,
            "roc_20d": 20,
            "roc_1m": 21,
            "roc_3m": 63,
            "roc_6m": 126,
            "roc_12m": 252,
        }

        for name, period in periods.items():
            df[name] = (
                price
                .pct_change(periods=period, fill_method=None)
                * 100
            )

        return df

    @staticmethod
    def _add_bollinger_z(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        price = df["adj_close"]

        ma20 = price.rolling(
            window=20,
            min_periods=20,
        ).mean()

        std20 = price.rolling(
            window=20,
            min_periods=20,
        ).std(ddof=0)

        df["bollinger_z"] = (
            (price - ma20)
            / std20.replace(0, np.nan)
        )

        return df

    @staticmethod
    def _add_rsi(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        price = df["adj_close"].to_numpy(
            dtype=np.float64
        )

        df["rsi"] = talib.RSI(
            price,
            timeperiod=14,
        )

        return df

    @staticmethod
    def _add_macd(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        price = df["adj_close"].to_numpy(
            dtype=np.float64
        )

        macd, signal, hist = talib.MACD(
            price,
            fastperiod=12,
            slowperiod=26,
            signalperiod=9,
        )

        df["macd"] = macd
        df["macd_signal"] = signal
        df["macd_hist"] = hist

        return df

    @staticmethod
    def _add_stochastic(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        high = df["adj_high"].to_numpy(
            dtype=np.float64
        )
        low = df["adj_low"].to_numpy(
            dtype=np.float64
        )
        close = df["adj_close"].to_numpy(
            dtype=np.float64
        )

        k, d = talib.STOCH(
            high,
            low,
            close,
            fastk_period=9,
            slowk_period=3,
            slowk_matype=0,
            slowd_period=3,
            slowd_matype=0,
        )

        df["stochastic_k"] = k
        df["stochastic_d"] = d

        # 台股常見 KDJ 定義
        df["stochastic_j"] = (
            3 * df["stochastic_k"]
            - 2 * df["stochastic_d"]
        )

        return df