from pydantic import BaseModel


class AnnouncementItem(BaseModel):
    title: str
    summary: str
    date: str
    url: str