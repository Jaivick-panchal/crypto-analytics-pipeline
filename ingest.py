import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

engine = create_engine('postgresql://postgres.fctqiafgpjhytxsbrrwd:Jaivick%402204@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres')

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": False
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    rows = []
    for coin in data:
        rows.append({
            'coin_id': coin['id'],
            'coin_name': coin['name'],
            'symbol': coin['symbol'],
            'current_price': coin['current_price'],
            'market_cap': coin['market_cap'],
            'total_volume': coin['total_volume'],
            'price_change_24h': coin['price_change_24h'],
            'price_change_pct_24h': coin['price_change_percentage_24h'],
            'high_24h': coin['high_24h'],
            'low_24h': coin['low_24h'],
            'circulating_supply': coin['circulating_supply'],
            'last_updated': coin['last_updated'],
            'ingested_at': datetime.now()
        })
    
    return pd.DataFrame(rows)

def load_to_postgres(df):
    df.to_sql('raw_crypto_prices', engine, if_exists='append', index=False)
    print(f"✅ {len(df)} rows loaded at {datetime.now().strftime('%H:%M:%S')}")

def run_pipeline():
    print(f"🚀 Pipeline starting at {datetime.now().strftime('%H:%M:%S')}")
    df = fetch_crypto_data()
    load_to_postgres(df)

scheduler = BlockingScheduler()
scheduler.add_job(run_pipeline, 'interval', minutes=5)

print("⏰ Scheduler started — fetching crypto prices every 5 minutes")
print("Press Ctrl+C to stop")

run_pipeline()
scheduler.start()
