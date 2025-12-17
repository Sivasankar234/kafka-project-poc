import sys
import os
import json
import signal
from dotenv import load_dotenv
from confluent_kafka import Consumer

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.logger import get_logger
from notification.email_service import EmailService

load_dotenv()
logger = get_logger("KafkaConsumer")


class KafkaConsumerService:
    def __init__(self):
        self.consumer = Consumer({
            "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            "group.id": os.getenv("KAFKA_GROUP_ID"),
            "auto.offset.reset": "earliest"
        })
        self.topic = os.getenv("KAFKA_TOPIC")
        self.email = EmailService()
        self.running = True

        logger.info("Kafka Consumer initialized")

    def start(self):
        logger.info("Starting Kafka consumer...")
        self.consumer.subscribe([self.topic])

        while self.running:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                logger.error(f"Kafka error: {msg.error()}")
                continue

            data = json.loads(msg.value().decode("utf-8"))
            logger.info(f"Message received: {data}")

            self.handle_event(data)

        self.consumer.close()
        logger.info("Kafka consumer closed")

    def handle_event(self, data):
        try:
            subject = f"GCS File {data['event'].upper()}"
            body = f"""
File Event Notification

Event   : {data['event']}
File    : {data['filename']}
Bucket  : {data['bucket']}
Time    : {data['timestamp']}
"""
            self.email.send_email(
                to_email="sivasankarsiva2001@gmail.com",
                subject=subject,
                message=body
            )
            logger.info("Email notification sent successfully")

        except Exception:
            logger.exception("Failed to process Kafka message")

    def shutdown(self, signum, frame):
        logger.info(f"Shutdown signal received ({signum})")
        self.running = False


if __name__ == "__main__":
    consumer_service = KafkaConsumerService()

    # Register graceful shutdown
    signal.signal(signal.SIGINT, consumer_service.shutdown)
    signal.signal(signal.SIGTERM, consumer_service.shutdown)

    consumer_service.start()
