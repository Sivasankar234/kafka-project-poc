import sys
import os

# Add project root to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gcs_utils.gcs_service import GCSService
from queues.kafka_producer import KafkaProducerService
from datetime import datetime
import os

gcs = GCSService()
producer = KafkaProducerService()

filename = "uploads/sample.txt"
result = gcs.delete_file(filename)

# Publish delete event
producer.publish({
    "event": "delete",
    "filename": filename,
    "bucket": os.getenv("GCS_BUCKET_NAME"),
    "timestamp": datetime.utcnow().isoformat()
})

print("Delete result:", result)
