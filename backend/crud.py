from sqlalchemy.orm import Session
import models, schemas
import bcrypt
import datetime

def get_password_hash(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Admin
def get_admin(db: Session, username: str):
    return db.query(models.Admin).filter(models.Admin.username == username).first()

def create_admin(db: Session, admin: schemas.AdminCreate):
    hashed_password = get_password_hash(admin.password)
    db_admin = models.Admin(username=admin.username, hashed_password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

# Bookings
def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def get_booking_by_date(db: Session, date: datetime.date):
    return db.query(models.Booking).filter(models.Booking.date == date).first()

def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).order_by(models.Booking.date.desc()).offset(skip).limit(limit).all()

def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(
        date=booking.date,
        customer_name=booking.customer_name,
        contact_phone=booking.contact_phone,
        id_card_number=booking.id_card_number,
        event_type=booking.event_type
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking_status(db: Session, booking_id: int, status: str):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking:
        db_booking.status = status
        db.commit()
        db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking:
        db.delete(db_booking)
        db.commit()
    return db_booking

# Settings
def get_setting(db: Session, key: str):
    return db.query(models.Setting).filter(models.Setting.key == key).first()

def get_settings(db: Session):
    return db.query(models.Setting).all()

def set_setting(db: Session, key: str, value: str):
    db_setting = db.query(models.Setting).filter(models.Setting.key == key).first()
    if db_setting:
        db_setting.value = value
    else:
        db_setting = models.Setting(key=key, value=value)
        db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

# Images
def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Image).order_by(models.Image.uploaded_at.desc()).offset(skip).limit(limit).all()

def create_image(db: Session, filename: str):
    db_image = models.Image(filename=filename)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def delete_image(db: Session, image_id: int):
    db_image = db.query(models.Image).filter(models.Image.id == image_id).first()
    if db_image:
        db.delete(db_image)
        db.commit()
    return db_image
