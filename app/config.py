from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "FinancialDashboard"
    contact_email: str = ""
    debug: bool = False

    # Supabase
    supabase_url: str
    supabase_key: str

    # Organizze API
    organizze_email: str
    organizze_token: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
