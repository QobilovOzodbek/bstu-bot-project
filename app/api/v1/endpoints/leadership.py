from fastapi import APIRouter

from app.services.scraper_service import scraper_service

router = APIRouter()


@router.get("/")
async def list_leadership():
    return await scraper_service.get_leadership()