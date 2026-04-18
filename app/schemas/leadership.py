from pydantic import BaseModel


class LeadershipItem(BaseModel):
    position: str
    full_name: str
    reception_time: str = ""
    phone: str = ""
    email: str = ""
    url: str