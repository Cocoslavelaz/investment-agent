import pandas as pd 
from FinMind.data import DataLoader
import requests
import os 
from functools import reduce
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('FINMIND_API_KEY')
API_KEY = api_key
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

    def get_macro_indicators(self,start_date,end_date=None):
        taiex = api.taiwan_stock_total_return_index(
                index_id="TAIEX",
                start_date=start_date,
                end_date=end_date
            ) #加權指數
        
        inst = api.taiwan_stock_institutional_investors_total(
        start_date=start_date,
        end_date=end_date,
        )

        ## 匯率
        url = "https://api.finmindtrade.com/api/v4/data"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        parameter = {
            "dataset": "TaiwanExchangeRate",
            "data_id": "USD",
            "start_date": start_date,
            "end_date":end_date
        }
        usd = requests.get(url, headers=headers, params=parameter)
        usd = usd.json()
        usd = pd.DataFrame(usd['data'])

        #美股
        url = 'https://api.finmindtrade.com/api/v4/data'
        dfs = []
        US_REGIME_LIST = [
            "SPY",    # US broad equity
            "QQQ",    # growth / tech risk appetite
            "SOXX",   # semiconductor cycle
            "TLT",    # long-duration Treasury proxy
            "UUP",    # USD proxy
            "VIXY",   # volatility proxy
        ]

        for stock_id in US_REGIME_LIST:
            parameter = {
                "dataset": "USStockPrice",
                "data_id": str(stock_id),
                "start_date": start_date,
                "end_date": end_date,
            }

            res = requests.get(url, headers=headers, params=parameter)
            data = res.json()

            # === 防呆 ===
            if "data" not in data or len(data["data"]) == 0:
                print(f"[WARNING] {stock_id} 沒有資料")
                continue

            df = pd.DataFrame(data['data'])

            # === 基本處理 ===
            df["date"] = pd.to_datetime(df["date"])

            # === drop stock_id ===
            if "stock_id" in df.columns:
                df = df.drop(columns=["stock_id"])

            # === 加 prefix ===
            prefix = stock_id.upper()
            df = df.rename(columns={
                col: f"{prefix}_{col}" for col in df.columns if col != "date"
            })

            dfs.append(df)

        if len(dfs) == 0:
            raise ValueError("所有股票都沒有抓到資料")

        # === merge 所有股票 ===
        df_merged = reduce(
            lambda left, right: pd.merge(left, right, on="date", how="outer"),
            dfs
        )
        df_merged = df_merged.sort_values("date").reset_index(drop=True)

        return taiex, inst, usd, df_merged       
            
        
        

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
        