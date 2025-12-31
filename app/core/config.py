from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application settings
    app_name: str = Field(default="Activity Logs POC", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")

    # Server Settings
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    # Database Settings
    database_url: str = Field(default="sqlite:///./test.db", alias="DATABASE_URL")
    database_echo: bool = Field(default=False, alias="DATABASE_ECHO")

    # Admin User Settings
    admin_email: str = Field(default="admin_user@example.com", alias="ADMIN_EMAIL")
    admin_password: str = Field(default="Admin@123", alias="ADMIN_PASSWORD")

    # JWT Settings
    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Kafka Settings
    kafka_enabled: bool = Field(default=False, alias="KAFKA_ENABLED")
    kafka_bootstrap_servers: str = Field(default="localhost:9092", alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_activity_topic: str = Field(default="user.activity", alias="KAFKA_ACTIVITY_TOPIC")
    kafka_client_id: str = Field(default="fastapi-activity-poc", alias="KAFKA_CLIENT_ID")
    kafka_group_id: str = Field(default="admin-monitor-group", alias="KAFKA_GROUP_ID")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()