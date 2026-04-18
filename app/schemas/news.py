from pydantic import BaseModel


class NewsItem(BaseModel):
    title: str
    summary: str
    date: str
    url: str