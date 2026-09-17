import pandas as pd 
from FinMind.data import DataLoader
import requests
import os 
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('FINMIND_API_KEY')
api = DataLoader()
api.login_by_token(api_token=api_key)

class FinMindClient:

    def get_stock_price(self,ticker, start_date,end_date=None):
        df = api.taiwan_stock_daily(
            stock_id=str(ticker),     
            start_date=start_date,
            end_date = end_date
        )   
        df["daily_return"] = df["close"].pct_change()
        df['date'] = pd.to_datetime(df['date'])
        return df

    def get_institutional_investors(
            self,
            ticker: str,
            start_date: str,
            end_date: str | None = None,
        ) -> pd.DataFrame:

        df = api.taiwan_stock_institutional_investors(
            stock_id=str(ticker),
            start_date=start_date,
            end_date=end_date,
        )

        if df is None or df.empty:
            return pd.DataFrame()
        return df

    def get_financial_statement():
        ...

    def get_dividend(self,ticker, start_date, end_date=None):
        df = api.taiwan_stock_dividend_result(
            stock_id=str(ticker),
            start_date=start_date,
            end_date=end_date
        )

        # ✅ 重要：可能是空表
        if df is None or len(df) == 0:
            return pd.DataFrame()

        return df
        