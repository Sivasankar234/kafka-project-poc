from gcs_utils.gcs_service import GCSService
from queues.kafka_producer import KafkaProducerService
from datetime import datetime
import os

gcs = GCSService()
producer = KafkaProducerService()

result = gcs.upload_file(
    local_path="sample.txt",
    gcs_path="uploads/sample.txt"
)

producer.publish({
    "event": "upload",
    "filename": "uploads/sample.txt",
    "bucket": os.getenv("GCS_BUCKET_NAME"),
    "timestamp": datetime.utcnow().isoformat()
})

print(result)
