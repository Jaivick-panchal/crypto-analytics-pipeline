SELECT
    coin_id,
    coin_name,
    symbol,
    current_price,
    price_change_pct_24h,
    volatility_pct,
    market_cap,
    total_volume,
    ingested_at,
    DATE_TRUNC('hour', ingested_at) AS ingested_hour
FROM {{ ref('stg_crypto_prices') }}
ORDER BY coin_id, ingested_at