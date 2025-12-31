from app.kafka.producer import KafkaProducerService

_kafka_producer: KafkaProducerService | None = None


def set_kafka_producer(producer: KafkaProducerService) -> None:
    global _kafka_producer
    _kafka_producer = producer


def get_kafka_producer_instance() -> KafkaProducerService:
    if _kafka_producer is None:
        raise RuntimeError("Kafka producer is not initialized")
    return _kafka_producer
