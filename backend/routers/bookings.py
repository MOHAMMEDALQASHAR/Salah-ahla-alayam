from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
import crud, schemas, database
import datetime
import os
import shutil
import uuid
from .auth import get_current_admin
from email_service import send_booking_notification
import threading

router = APIRouter(prefix="/bookings", tags=["bookings"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/check/{date}", response_model=dict)
def check_availability(date: datetime.date, db = Depends(database.get_db)):
    booking = crud.get_booking_by_date(db, date=date)
    if booking:
        return {"available": False, "status": booking["status"]}
    return {"available": True}

@router.post("/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db = Depends(database.get_db)):
    existing_booking = crud.get_booking_by_date(db, date=booking.date)
    if existing_booking:
        raise HTTPException(status_code=400, detail="Date already booked")
    new_booking = crud.create_booking(db=db, booking=booking)
    # إرسال إيميل الإشعار في الخلفية
    threading.Thread(target=send_booking_notification, args=(new_booking,), daemon=True).start()
    return new_booking

@router.post("/with-receipt", response_model=schemas.Booking)
def create_booking_with_receipt(
    date: datetime.date = Form(...),
    customer_name: str = Form(...),
    contact_phone: str = Form(...),
    id_card_number: str = Form(""),
    event_type: str = Form(""),
    pay_deposit: str = Form("لا"),
    receipt: Optional[UploadFile] = File(None),
    db = Depends(database.get_db)
):
    existing_booking = crud.get_booking_by_date(db, date=date)
    if existing_booking:
        raise HTTPException(status_code=400, detail="Date already booked")
    
    receipt_filename = ""
    if receipt and receipt.filename:
        ext = os.path.splitext(receipt.filename)[1]
        unique_name = f"receipt_{uuid.uuid4().hex[:8]}{ext}"
        file_location = os.path.join(UPLOAD_DIR, unique_name)
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(receipt.file, file_object)
        receipt_filename = unique_name
        
    booking_in = schemas.BookingCreate(
        date=date,
        customer_name=customer_name,
        contact_phone=contact_phone,
        id_card_number=id_card_number,
        event_type=event_type,
        pay_deposit=pay_deposit,
        deposit_receipt=receipt_filename
    )
    new_booking = crud.create_booking(db=db, booking=booking_in)
    # إرسال إيميل الإشعار في الخلفية
    threading.Thread(target=send_booking_notification, args=(new_booking,), daemon=True).start()
    return new_booking

@router.get("/", response_model=List[schemas.Booking])
def read_bookings(skip: int = 0, limit: int = 100, db = Depends(database.get_db), current_admin = Depends(get_current_admin)):
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings

@router.put("/{booking_id}/status", response_model=schemas.Booking)
def update_status(booking_id: str, status: str, db = Depends(database.get_db), current_admin = Depends(get_current_admin)):
    booking = crud.update_booking_status(db, booking_id=booking_id, status=status)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.delete("/{booking_id}", response_model=schemas.Booking)
def delete_booking(booking_id: str, db = Depends(database.get_db), current_admin = Depends(get_current_admin)):
    booking = crud.delete_booking(db, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking
