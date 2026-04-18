import httpx

from app.core.config import settings


class BaseScraper:
    async def fetch_html(self, url: str) -> str:
        headers = {
            "User-Agent": settings.scraper_user_agent,
            "Accept-Language": "uz,en;q=0.9",
        }

        async with httpx.AsyncClient(
            timeout=settings.scraper_timeout,
            follow_redirects=True,
            headers=headers,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text