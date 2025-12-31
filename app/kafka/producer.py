import json
import asyncio
from aiokafka.errors import KafkaConnectionError
from aiokafka import AIOKafkaProducer


class KafkaProducerService:
    def __init__(
        self,
        *,
        bootstrap_servers: str,
        client_id: str,
        enabled: bool = True,
    ):
        self._enabled = enabled
        self._producer: AIOKafkaProducer | None = None

        if enabled:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=bootstrap_servers,
                client_id=client_id,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )

    async def start(self, retries: int = 10, delay: int = 3):
        if not self._enabled or not self._producer:
            return

        for attempt in range(1, retries + 1):
            try:
                await self._producer.start()
                print("🟢 Kafka producer connected")
                return
            except KafkaConnectionError as e:
                print(f"⏳ Kafka not ready (attempt {attempt}/{retries})")
                await asyncio.sleep(delay)

        print("❌ Kafka producer failed after retries")


    async def stop(self):
        if self._producer:
            await self._producer.stop()
            print("🔴 Kafka producer stopped")

    async def publish(self, *, topic: str, message: dict):
        if not self._enabled:
            return

        if not self._producer:
            raise RuntimeError("Kafka producer not initialized")

        await self._producer.send_and_wait(topic, message)

