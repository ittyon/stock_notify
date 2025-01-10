import yfinance as yf
import requests
import os
from dotenv import load_dotenv
from config import tickers
import datetime

# 土日であれば処理しない
today = datetime.datetime.today()
if today.weekday() > 4:
    print("土日なので処理なし")
    exit()

# .envファイル読み込み
load_dotenv('.env')

# lineメッセージ変数
today = today.strftime("%Y/%m/%d")
message =   f"\n\n{today} 株価結果情報"

try:

    for ticker in tickers:

        # yfinanceで株情報を取得
        stock = yf.Ticker(ticker)

        # 銘柄名の取得
        company_name = stock.info.get('longName', stock.info.get('symbol', 'Unknown'))

        # 本日の株価データを取得（最新データ）
        today_data = stock.history(period="1d")

        # 本日の最高株価と最低株価を取得
        high_price = today_data['High'].iloc[0]
        low_price = today_data['Low'].iloc[0]

        # 結果を表示
        print(f"銘柄名: {company_name}")
        print(f"本日の最高株価: {high_price} 円")
        print(f"本日の最低株価: {low_price} 円")

        # 銘柄と株価をメッセージに追記
        message += f"\n\n{company_name}\n最高株価：{high_price}円\n最低株価：{low_price}円"

except Exception as e:
    
    print("予期せぬエラー発生")
    message += "予期せぬエラーが発生したため処理終了とします。"

finally:
    
    # lineに通知
    
    # 1.リクエスト情報設定
    url = os.getenv('URL')
    access_token = os.getenv('ACCESS_TOKEN')
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {'message': message}

    # 2.リクエスト実行
    result = requests.post(url, headers=headers, params=params)

    print("処理終了")

