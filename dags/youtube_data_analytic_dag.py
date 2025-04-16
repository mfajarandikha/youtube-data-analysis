import requests
import logging
import pandas as pd
from io import BytesIO
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)
from airflow.operators.bash import BashOperator
from google.cloud import storage
import json

with open("/opt/airflow/creds.json") as f:
    creds = json.load(f)

logging.basicConfig(level=logging.INFO)

# Constants and configurations
PROJECT_ID = creds["project_id"]
API_KEY = creds["api_key"]
CHANNEL_ID = creds["channel_id"]
START_DATE = "2025-01-21T00:00:00Z"
END_DATE = "2025-03-29T00:00:00Z"
GCS_BUCKET_NAME = "final-project-bucket-resource"  
GCS_FOLDER = "data"  


# Fetch data from YouTube API
def fetch_youtube_data():
    video_details = []
    page_token = None

    while True:
        search_url = (
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}"
            f"&type=video&eventType=completed&publishedAfter={START_DATE}&publishedBefore={END_DATE}"
            f"&maxResults=50&key={API_KEY}"
        )
        if page_token:
            search_url += f"&pageToken={page_token}"

        search_response = requests.get(search_url).json()
        video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]

        if video_ids:
            stats_url = (
                f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics"
                f"&id={','.join(video_ids)}&key={API_KEY}"
            )
            stats_response = requests.get(stats_url).json()

            for item in stats_response.get("items", []):
                video_info = {
                    "video_id": item["id"],
                    "title": item["snippet"]["title"],
                    "video_url": f"https://www.youtube.com/watch?v={item['id']}",
                    "published_date": item["snippet"].get("publishedAt", "N/A"),
                    "views": item["statistics"].get("viewCount", "0"),
                    "likes": item["statistics"].get("likeCount", "0"),
                    "comments": item["statistics"].get("commentCount", "0"),
                }
                video_details.append(video_info)

        page_token = search_response.get("nextPageToken")
        if not page_token:
            break

    df = pd.DataFrame(video_details)
    if df.empty:
        logging.warning("No data fetched.")
    else:
        logging.info(f"Fetched {len(df)} videos.")
    return df


def upload_to_gcs_from_df(df, bucket_name, blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)  

    blob.upload_from_file(buffer, content_type="text/csv")
    logging.info(f"Uploaded data to gs://{bucket_name}/{blob_name}")


def save_youtube_data_and_upload():
    df = fetch_youtube_data()
    if df.empty:
        return "No data to save."

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"youtube_data_{timestamp}.csv"
    gcs_path = f"{GCS_FOLDER}/{filename}"

    upload_to_gcs_from_df(df, GCS_BUCKET_NAME, gcs_path)

    return f"Saved and uploaded to GCS: {gcs_path}"


with DAG(
    dag_id="youtube_to_gcs_dag",
    start_date=datetime(2025, 4, 1),
    schedule_interval="@monthly",
    catchup=False,
    description="Fetch YouTube data and upload to Google Cloud Storage",
    tags=["youtube", "gcs"],
) as dag:

    extract_save_upload_task = PythonOperator(
        task_id="fetch_save_upload_youtube_data",
        python_callable=save_youtube_data_and_upload,
    )

    upload_to_bigquery = GCSToBigQueryOperator(
        task_id="upload_youtube_csv_to_bigquery",
        bucket=GCS_BUCKET_NAME,
        source_objects=[f"{GCS_FOLDER}/*.csv"],
        destination_project_dataset_table=f"{PROJECT_ID}.youtube_data.live_stream_stats",
        source_format="CSV",
        skip_leading_rows=1,
        write_disposition="WRITE_APPEND",
        create_disposition="CREATE_IF_NEEDED",
        autodetect=True,
        gcp_conn_id="google_cloud_default",
    )

    run_dbt_transformation = BashOperator(
        task_id="run_dbt_transform",
        bash_command="cd /opt/airflow/dbt && dbt run --profiles-dir .",
    )

    extract_save_upload_task >> upload_to_bigquery >> run_dbt_transformation
