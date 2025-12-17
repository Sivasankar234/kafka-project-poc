import sys
import os

from dotenv import load_dotenv
# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from confluent_kafka import Consumer
from config.logger import get_logger
from notification.email_service import EmailService
load_dotenv()
logger = get_logger("KafkaConsumer")

# logger.info(f"KAFKA_BOOTSTRAP_SERVERS: {os.getenv('KAFKA_BOOTSTRAP_SERVERS')}")
# logger.info(f"KAFKA_GROUP_ID: {os.getenv('KAFKA_GROUP_ID')}")
# logger.info(f"KAFKA_TOPIC: {os.getenv('KAFKA_TOPIC')}")

class KafkaConsumerService:
    def __init__(self):
        self.consumer = Consumer({
            "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            "group.id": os.getenv("KAFKA_GROUP_ID"),
            "auto.offset.reset": "earliest"
        })
        self.topic = os.getenv("KAFKA_TOPIC")
        self.email = EmailService()
        logger.info("Kafka Consumer initialized")

    def start(self):
        logger.info("Starting Kafka consumer...")
        self.consumer.subscribe([self.topic])

        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                logger.error(f"Kafka error: {msg.error()}")
                continue

            data = json.loads(msg.value().decode("utf-8"))
            logger.info(f"Message received: {data}")

            self.handle_event(data)

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

        except Exception as e:
            logger.exception("Failed to process Kafka message")
    def shutdown(signal, frame):
        logger.info("Shutting down consumer...")
        consumer.close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

if __name__ == "__main__":
    consumer = KafkaConsumerService()
    consumer.start()
