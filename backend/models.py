from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Float, func
from database import Base
import datetime

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True) # One booking per day for a wedding hall
    customer_name = Column(String, index=True)
    contact_phone = Column(String)
    id_card_number = Column(String)
    event_type = Column(String)
    status = Column(String, default="pending") # pending, confirmed, cancelled
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
