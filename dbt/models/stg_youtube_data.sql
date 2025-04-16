select
  video_id,
  title,
  video_url,
  published_date,
  views,
  likes,
  comments
from {{ source('youtube_data', 'live_stream_stats') }}
