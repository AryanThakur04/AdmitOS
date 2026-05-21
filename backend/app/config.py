from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "postgresql://admitos:admitos_secret@localhost:5432/admitos"
    secret_key: str = "demo-secret-key"
    cors_origins: str = "http://localhost:5173"
    gemini_api_key: str = ""
    openai_api_key: str = ""
    ai_provider: str = "gemini"
    google_sheets_credentials_json: str = ""
    google_sheet_id: str = ""
    whatsapp_api_token: str = ""

    @property
    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
