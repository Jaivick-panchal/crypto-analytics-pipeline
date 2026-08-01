SELECT
    coin_id,
    coin_name,
    symbol,
    current_price,
    market_cap,
    total_volume,
    price_change_24h,
    price_change_pct_24h,
    high_24h,
    low_24h,
    circulating_supply,
    CAST(last_updated AS TIMESTAMP) AS last_updated,
    ingested_at,
    ROUND(CAST(high_24h - low_24h AS NUMERIC), 8) AS price_range_24h,
    ROUND(CAST((high_24h - low_24h) / NULLIF(low_24h, 0) * 100 AS NUMERIC), 4) AS volatility_pct
FROM {{ source('public', 'raw_crypto_prices') }}