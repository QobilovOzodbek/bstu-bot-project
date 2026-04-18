from pydantic import BaseModel


class ContactInfo(BaseModel):
    address: str = ""
    email: str = ""
    phone: str = ""