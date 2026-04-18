from fastapi import APIRouter

from app.api.v1.endpoints import announcements, contact, leadership, links, news

api_router = APIRouter()
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(announcements.router, prefix="/announcements", tags=["announcements"])
api_router.include_router(leadership.router, prefix="/leadership", tags=["leadership"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
api_router.include_router(links.router, prefix="/links", tags=["links"])