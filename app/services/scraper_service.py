from datetime import datetime, timedelta
from typing import Any

from app.core.config import settings
from app.scrapers.bstu_scraper import BSTUScraper


class SimpleTTLCache:
    def __init__(self, hours: int):
        self.ttl = timedelta(hours=hours)
        self.storage: dict[str, dict[str, Any]] = {}

    def get(self, key: str):
        item = self.storage.get(key)
        if not item:
            return None

        if datetime.utcnow() > item["expires_at"]:
            self.storage.pop(key, None)
            return None

        return item["value"]

    def set(self, key: str, value: Any):
        self.storage[key] = {
            "value": value,
            "expires_at": datetime.utcnow() + self.ttl,
        }


class ScraperService:
    def __init__(self):
        self.scraper = BSTUScraper()
        self.cache = SimpleTTLCache(hours=settings.cache_hours)

    async def _get_or_set(self, key: str, getter):
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        data = await getter()
        self.cache.set(key, data)
        return data

    async def get_news(self):
        return await self._get_or_set("news", self.scraper.get_news)

    async def get_announcements(self):
        return await self._get_or_set("announcements", self.scraper.get_announcements)

    async def get_leadership(self):
        return await self._get_or_set("leadership", self.scraper.get_leadership)

    async def get_contact_info(self):
        return await self._get_or_set("contact_info", self.scraper.get_contact_info)

    async def get_quick_links(self):
        return await self._get_or_set("quick_links", self.scraper.get_quick_links)


scraper_service = ScraperService()