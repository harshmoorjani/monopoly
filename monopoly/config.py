from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gmail_address: str
    project_id: str
    pubsub_topic: str
    secret_id: str
    gcs_bucket: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()