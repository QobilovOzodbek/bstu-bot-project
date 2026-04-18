from fastapi import APIRouter

from app.services.scraper_service import scraper_service

router = APIRouter()


@router.get("/")
async def list_quick_links():
    return await scraper_service.get_quick_links()