import httpx
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class APIClient:
    def __init__(self):
        self.base_url = getenv("API_BASE_URL", "http://127.0.0.1:8000")

    async def _get(self, path: str):
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    async def get_news(self):
        return await self._get("/api/v1/news/")

    async def get_announcements(self):
        return await self._get("/api/v1/announcements/")

    async def get_leadership(self):
        return await self._get("/api/v1/leadership/")

    async def get_contact_info(self):
        return await self._get("/api/v1/contact/")

    async def get_quick_links(self):
        return await self._get("/api/v1/links/")


api_client = APIClient()