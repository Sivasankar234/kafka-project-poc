import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
class GCSConfig:
    # GCS Configuration
    GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
    GCS_SERVICE_ACCOUNT = os.getenv("GCS_SERVICE_ACCOUNT")
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")

    # Email Configuration
    GMAIL_USER = os.getenv("GMAIL_USER")
    GMAIL_PASS = os.getenv("GMAIL_PASS")

    # Kafka Configuration (Confluent Cloud)
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
    KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")

    # Legacy Pub/Sub (for reference, can be removed later)
    PUBSUB_SUBSCRIPTION = os.getenv("PUBSUB_SUBSCRIPTION")
    PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC")