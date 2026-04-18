from pydantic import BaseModel


class QuickLink(BaseModel):
    title: str
    url: str