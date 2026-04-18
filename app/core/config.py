from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    api_host: str = getenv("API_HOST", "127.0.0.1")
    api_port: int = int(getenv("API_PORT", "8000"))
    scraper_user_agent: str = getenv("SCRAPER_USER_AGENT", "Mozilla/5.0")
    scraper_timeout: int = int(getenv("SCRAPER_TIMEOUT", "30"))
    cache_hours: int = int(getenv("CACHE_HOURS", "20"))


settings = Settings()