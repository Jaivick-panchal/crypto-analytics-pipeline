import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

engine = create_engine('postgresql://postgres:Jaivick%402204@db.fctqiafgpjhytxsbrrwd.supabase.co:5432/postgres')

st.set_page_config(page_title="Crypto Analytics Dashboard", layout="wide", page_icon="📈")
st.title("📈 Crypto Analytics Dashboard")
st.caption("Live data powered by CoinGecko API → PostgreSQL → dbt → Streamlit")

# --- Load Data ---
@st.cache_data(ttl=300)
def load_latest():
    return pd.read_sql("SELECT * FROM mart_latest_prices ORDER BY market_cap DESC", engine)

@st.cache_data(ttl=300)
def load_history():
    return pd.read_sql("SELECT * FROM mart_price_history ORDER BY ingested_at", engine)

df_latest = load_latest()
df_history = load_history()

# --- KPI Cards ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Coins Tracked", len(df_latest))
col2.metric("Highest Price", f"${df_latest['current_price'].max():,.2f}")
col3.metric("Most Volatile", df_latest.loc[df_latest['volatility_pct'].idxmax(), 'coin_name'])
col4.metric("Total Market Cap", f"${df_latest['market_cap'].sum()/1e12:.2f}T")

st.divider()

# --- Latest Prices Table ---
st.subheader("💰 Latest Prices")
st.dataframe(
    df_latest[['coin_name', 'symbol', 'current_price', 'price_change_pct_24h', 'market_cap', 'total_volume', 'volatility_pct']].style.format({
        'current_price': '${:,.4f}',
        'price_change_pct_24h': '{:.2f}%',
        'market_cap': '${:,.0f}',
        'total_volume': '${:,.0f}',
        'volatility_pct': '{:.2f}%'
    }),
    use_container_width=True
)

st.divider()

# --- Price Change Bar Chart ---
st.subheader("📊 24h Price Change %")
fig1 = px.bar(
    df_latest.sort_values('price_change_pct_24h'),
    x='price_change_pct_24h',
    y='coin_name',
    orientation='h',
    color='price_change_pct_24h',
    color_continuous_scale=['red', 'gray', 'green'],
    title="24h Price Change by Coin"
)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# --- Price History Line Chart ---
st.subheader("📈 Price History")
coins = df_history['coin_name'].unique().tolist()
selected_coins = st.multiselect("Select coins to compare", coins, default=["Bitcoin", "Ethereum", "Solana"])

filtered = df_history[df_history['coin_name'].isin(selected_coins)]
fig2 = px.line(
    filtered,
    x='ingested_at',
    y='current_price',
    color='coin_name',
    title="Price Over Time"
)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- Volatility Chart ---
st.subheader("⚡ Volatility by Coin")
fig3 = px.bar(
    df_latest.sort_values('volatility_pct', ascending=False),
    x='coin_name',
    y='volatility_pct',
    color='volatility_pct',
    color_continuous_scale='Oranges',
    title="24h Volatility % (Higher = Riskier)"
)
st.plotly_chart(fig3, use_container_width=True)
