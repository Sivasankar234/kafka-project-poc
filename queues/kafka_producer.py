import json
import os
from confluent_kafka import Producer
from dotenv import load_dotenv
from config.logger import get_logger

load_dotenv()
logger = get_logger("KafkaProducer")

class KafkaProducerService:
    def __init__(self):
        self.topic = os.getenv("KAFKA_TOPIC")
        logger.info(f"Topic: {self.topic}")
        self.producer = Producer({
            "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        })
        logger.info("Kafka Producer initialized")

    def delivery_report(self, err, msg):
        if err:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(
                f"Message delivered to {msg.topic()} [{msg.partition()}]"
            )

    def publish(self, message: dict):
        logger.info(f"Publishing message: {message}")
        self.producer.produce(
            topic=self.topic,
            value=json.dumps(message),
            callback=self.delivery_report
        )
        self.producer.flush()
