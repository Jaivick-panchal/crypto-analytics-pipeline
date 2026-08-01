WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY coin_id ORDER BY ingested_at DESC) AS rn
    FROM {{ ref('stg_crypto_prices') }}
)
SELECT
    coin_id,
    coin_name,
    symbol,
    current_price,
    market_cap,
    total_volume,
    price_change_pct_24h,
    volatility_pct,
    price_range_24h,
    high_24h,
    low_24h,
    ingested_at
FROM ranked
WHERE rn = 1