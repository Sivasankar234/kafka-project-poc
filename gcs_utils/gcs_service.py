from google.cloud import storage
from config.logger import get_logger
from config.gcs_config import GCS_SERVICE_ACCOUNT, GCS_BUCKET_NAME

logger = get_logger("GCSService")

class GCSService:
    def __init__(self, bucket_name=GCS_BUCKET_NAME):
        self.client = storage.Client.from_service_account_json(
            GCS_SERVICE_ACCOUNT
        )
        self.bucket = self.client.bucket(bucket_name)
        logger.info(f"Connected to GCS bucket: {bucket_name}")

    def upload_file(self, local_path, gcs_path):
        logger.info(f"Uploading file {local_path} to {gcs_path}")
        blob = self.bucket.blob(gcs_path)
        blob.upload_from_filename(local_path)
        logger.info("Upload successful")
        return f"Uploaded to gs://{GCS_BUCKET_NAME}/{gcs_path}"

    def read_file(self, gcs_path, download_to):
        logger.info(f"Downloading file {gcs_path}")
        blob = self.bucket.blob(gcs_path)
        blob.download_to_filename(download_to)
        logger.info("Download successful")

    def delete_file(self, gcs_path):
        logger.warning(f"Deleting file {gcs_path}")
        blob = self.bucket.blob(gcs_path)
        blob.delete()
        logger.info("Delete successful")
