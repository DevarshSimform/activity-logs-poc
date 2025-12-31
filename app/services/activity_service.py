import asyncio
import json
from app.database import SessionLocal
from app.database.models.activity import ActivityType
from app.repositories.activity_repository import ActivityRepository
from app.kafka.schemas import BaseEvent


class ActivityService:
    @staticmethod
    async def log_profile_updated(
        *,
        user_id: int,
        request_id: str,
        data: dict | None,
        kafka_producer,
        topic: str,
        actor: dict,
        meta: dict,
    ) -> None:
        db = SessionLocal()
        try:
            # Create activity log in DB
            ActivityRepository.create(
                db=db,
                user_id=user_id,
                activity_type=ActivityType.PROFILE_UPDATED,
                action="User profile updated",
                request_id=request_id,
                data=json.dumps(data) if data else None,
            )

            db.commit()

            # Build event
            event = BaseEvent(
                event_type="profile.updated",
                actor=actor,
                resource={"type": "user", "id": user_id},
                payload={"changes": data},
                request_id=request_id,
                meta=meta,
            )

            # Publish to Kafka asynchronously without blocking main thread
            await kafka_producer.publish(
                topic=topic,
                message=event.to_dict(),
            )

        except Exception as e:
            db.rollback()
            # NEVER crash background thread
            print("❌ Failed to log activity:", str(e))

        finally:
            db.close()

