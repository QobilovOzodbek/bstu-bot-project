from pydantic import BaseModel


class ClubItem(BaseModel):
    title: str
    category: str = ""
    description: str = ""
    source: str = ""
    url: str