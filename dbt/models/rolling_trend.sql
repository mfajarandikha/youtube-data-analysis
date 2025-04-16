WITH daily_views AS (
  SELECT
    DATE(published_date) AS publish_date,
    SUM(views) AS total_views
  FROM {{ ref('stg_youtube_data') }}
  GROUP BY publish_date
),

rolling_avg AS (
  SELECT
    publish_date,
    total_views,
    AVG(total_views) OVER (
      ORDER BY publish_date 
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7_day_avg
  FROM daily_views
)

SELECT * FROM rolling_avg
ORDER BY publish_date
