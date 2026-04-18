from fastapi import APIRouter

from app.services.scraper_service import scraper_service

router = APIRouter()


@router.get("/")
async def get_contact_info():
    return await scraper_service.get_contact_info()