from pydantic import BaseModel
from typing import Optional, List
import datetime

# Admin Schemas
class AdminBase(BaseModel):
    username: str

class AdminCreate(AdminBase):
    password: str

class Admin(AdminBase):
    id: int

    class Config:
        from_attributes = True

# Booking Schemas
class BookingBase(BaseModel):
    date: datetime.date
    customer_name: str
    contact_phone: str
    id_card_number: Optional[str] = ""
    event_type: Optional[str] = ""

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    status: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# Setting Schemas
class SettingBase(BaseModel):
    key: str
    value: str

class SettingCreate(SettingBase):
    pass

class Setting(SettingBase):
    id: int

    class Config:
        from_attributes = True

# Image Schemas
class ImageBase(BaseModel):
    filename: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    uploaded_at: datetime.datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
