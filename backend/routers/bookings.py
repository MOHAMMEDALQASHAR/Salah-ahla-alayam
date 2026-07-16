from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas, database
import datetime
from .auth import get_current_admin

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.get("/check/{date}", response_model=dict)
def check_availability(date: datetime.date, db: Session = Depends(database.get_db)):
    booking = crud.get_booking_by_date(db, date=date)
    if booking:
        return {"available": False, "status": booking.status}
    return {"available": True}

@router.post("/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(database.get_db)):
    existing_booking = crud.get_booking_by_date(db, date=booking.date)
    if existing_booking:
        raise HTTPException(status_code=400, detail="Date already booked")
    return crud.create_booking(db=db, booking=booking)

@router.get("/", response_model=List[schemas.Booking])
def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_admin: models.Admin = Depends(get_current_admin)):
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings

@router.put("/{booking_id}/status", response_model=schemas.Booking)
def update_status(booking_id: int, status: str, db: Session = Depends(database.get_db), current_admin: models.Admin = Depends(get_current_admin)):
    booking = crud.update_booking_status(db, booking_id=booking_id, status=status)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.delete("/{booking_id}", response_model=schemas.Booking)
def delete_booking(booking_id: int, db: Session = Depends(database.get_db), current_admin: models.Admin = Depends(get_current_admin)):
    booking = crud.delete_booking(db, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking
