
WITH base AS (
  SELECT
    DATE(published_date) AS publish_date,
    EXTRACT(DAYOFWEEK FROM published_date) AS day_of_week, 
    FORMAT_DATE('%A', DATE(published_date)) AS day_name,
    views
  FROM {{ ref('stg_youtube_data') }}
),

views_grouped AS (
  SELECT
    day_of_week,
    day_name,
    SUM(views) AS total_views
  FROM base
  GROUP BY day_of_week, day_name
)

SELECT
  day_of_week,
  day_name,
  total_views
FROM views_grouped
ORDER BY total_views DESC
