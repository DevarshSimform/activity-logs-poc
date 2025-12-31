import json
from aiokafka import AIOKafkaConsumer

from app.websockets import admin_ws_manager


class KafkaConsumerService:
    def __init__(
        self,
        *,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        enabled: bool = True,
    ):
        self._enabled = enabled
        self._topic = topic
        self._consumer: AIOKafkaConsumer | None = None

        if enabled:
            self._consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers,
                group_id=group_id,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                auto_offset_reset="earliest",
            )

    async def start(self):
        if not self._enabled or not self._consumer:
            return

        await self._consumer.start()
        print("🟢 Kafka consumer started")

        async for message in self._consumer:
            print("📩 Event triggered")
            print("Topic:", message.topic)
            print("Payload:", message.value)

            print("➡️ Calling admin_ws_manager.broadcast()")
            await admin_ws_manager.broadcast({
                "topic": message.topic,
                "event": message.value,
            })


    async def stop(self):
        if self._consumer:
            await self._consumer.stop()
            print("🔴 Kafka consumer stopped")
