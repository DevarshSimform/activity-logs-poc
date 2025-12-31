import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import api_router
from app.api.v1.endpoints import admin_router
from app.core.config import settings
from app.database.models import Base, engine
from app.database.scripts import create_admin_user
from app.middleware import setup_middlewares
from app.exceptions import setup_exception_handlers
from app.kafka import KafkaProducerService, KafkaConsumerService
from app.kafka.registry import set_kafka_producer
from app.websockets.routes import router as websocket_router

# Import Kafka consumer/producer startup functions if needed
# from app.kafka.consumer import start_kafka_consumer
# from app.kafka.producer import init_kafka_producer

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    # Initialize Kafka Producer singleton per application
    kafka_producer = KafkaProducerService(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        client_id=settings.kafka_client_id,
        enabled=settings.kafka_enabled,
    )
    # Initialize Kafka Consumer singleton per application
    kafka_consumer = KafkaConsumerService(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        topic=settings.kafka_activity_topic,
        group_id=settings.kafka_group_id,
        enabled=settings.kafka_enabled,
    )

    # Startup
    print(f"🚀 Starting FastAPI ...")
    print(f"App: {settings.app_name}")
    print(f"Version: v{settings.app_version}")
    print(f"Debug mode: {settings.debug}")

    # Create SQLAlchemy tables (sync)
    print("Creating database tables (if not exists)...")
    Base.metadata.create_all(bind=engine)
    print("Tables created")

    # Create Admin User
    create_admin_user()

    # Start Kafka Producer
    # await init_kafka_producer()
    try:
        await kafka_producer.start()
        set_kafka_producer(kafka_producer)
        print("🟢 Kafka producer started")
    except Exception as e:
        print("⚠️ Kafka not available, continuing without Kafka:", e)


    consumer_task = asyncio.create_task(kafka_consumer.start())

    # Start Kafka Consumer (async loop)
    # asyncio.create_task(start_kafka_consumer())
    # print("Kafka consumer started")


    yield


    # Close Kafka Connections
    # await close_kafka_producer()
    consumer_task.cancel()
    await kafka_producer.stop()
    await kafka_consumer.stop()

    print("🛑 FastAPI shutting down...")


def create_app() -> FastAPI:
    """ Create and configure the FastAPI application """

    # Create FastAPI instance
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="A POC demonstrating FastAPI + Kafka + WebSockets + Background Tasks",
        debug=settings.debug,
        lifespan=lifespan,  # Using event handlers instead of lifespan context
    )

    # Setup CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup Custom middlewares
    setup_middlewares(app)

    # Include Routers
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(admin_router)
    app.include_router(websocket_router)

    # Setup Exception Handlers
    setup_exception_handlers(app)

    # Mount Static Files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Health Check Endpoint
    @app.get("/", tags=["health"])
    async def health():
        return {"status": "ok", "message": "FastAPI POC is running"}

    return app


app = create_app()
    
