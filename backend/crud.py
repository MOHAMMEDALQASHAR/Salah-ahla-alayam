from bson.objectid import ObjectId
import bcrypt
import datetime
import schemas

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# --- Helper Formatters ---
def _format_admin(doc):
    if not doc:
        return None
    doc = dict(doc)
    doc["id"] = str(doc["_id"])
    return doc

def _format_booking(doc):
    if not doc:
        return None
    doc = dict(doc)
    doc["id"] = str(doc["_id"])
    if isinstance(doc.get("date"), str):
        doc["date"] = datetime.date.fromisoformat(doc["date"])
    if isinstance(doc.get("created_at"), str):
        doc["created_at"] = datetime.datetime.fromisoformat(doc["created_at"])
    doc["pay_deposit"] = doc.get("pay_deposit", "لا")
    doc["deposit_receipt"] = doc.get("deposit_receipt", "")
    return doc

def _format_setting(doc):
    if not doc:
        return None
    doc = dict(doc)
    doc["id"] = str(doc["_id"])
    return doc

def _format_image(doc):
    if not doc:
        return None
    doc = dict(doc)
    doc["id"] = str(doc["_id"])
    doc["row"] = doc.get("row", "top")
    if isinstance(doc.get("uploaded_at"), str):
        doc["uploaded_at"] = datetime.datetime.fromisoformat(doc["uploaded_at"])
    return doc

# --- Admin ---
def get_admin(db, username: str):
    doc = db.admins.find_one({"username": username})
    return _format_admin(doc)

def create_admin(db, admin: schemas.AdminCreate):
    hashed_password = get_password_hash(admin.password)
    doc = {"username": admin.username, "hashed_password": hashed_password}
    res = db.admins.insert_one(doc)
    return _format_admin(doc)

# --- Bookings ---
def get_booking(db, booking_id: str):
    try:
        obj_id = ObjectId(booking_id)
    except Exception:
        return None
    doc = db.bookings.find_one({"_id": obj_id})
    return _format_booking(doc)

def get_booking_by_date(db, date: datetime.date):
    date_str = date.isoformat()
    doc = db.bookings.find_one({"date": date_str})
    return _format_booking(doc)

def get_bookings(db, skip: int = 0, limit: int = 100):
    cursor = db.bookings.find().sort("date", -1).skip(skip).limit(limit)
    return [_format_booking(doc) for doc in cursor]

def create_booking(db, booking: schemas.BookingCreate):
    now = datetime.datetime.utcnow()
    doc = {
        "date": booking.date.isoformat(),
        "customer_name": booking.customer_name,
        "contact_phone": booking.contact_phone,
        "id_card_number": booking.id_card_number or "",
        "event_type": booking.event_type or "",
        "pay_deposit": booking.pay_deposit or "لا",
        "deposit_receipt": booking.deposit_receipt or "",
        "status": "pending",
        "created_at": now
    }
    db.bookings.insert_one(doc)
    return _format_booking(doc)

def update_booking_status(db, booking_id: str, status: str):
    try:
        obj_id = ObjectId(booking_id)
    except Exception:
        return None
    db.bookings.update_one({"_id": obj_id}, {"$set": {"status": status}})
    doc = db.bookings.find_one({"_id": obj_id})
    return _format_booking(doc)

def delete_booking(db, booking_id: str):
    try:
        obj_id = ObjectId(booking_id)
    except Exception:
        return None
    doc = db.bookings.find_one({"_id": obj_id})
    if doc:
        db.bookings.delete_one({"_id": obj_id})
        return _format_booking(doc)
    return None

# --- Settings ---
def get_setting(db, key: str):
    doc = db.settings.find_one({"key": key})
    return _format_setting(doc)

def get_settings(db):
    cursor = db.settings.find()
    return [_format_setting(doc) for doc in cursor]

def set_setting(db, key: str, value: str):
    db.settings.update_one({"key": key}, {"$set": {"value": value}}, upsert=True)
    doc = db.settings.find_one({"key": key})
    return _format_setting(doc)

# --- Images ---
def get_images(db, skip: int = 0, limit: int = 100):
    cursor = db.images.find().sort("uploaded_at", -1).skip(skip).limit(limit)
    return [_format_image(doc) for doc in cursor]

def create_image(db, filename: str, row: str = "top"):
    doc = {
        "filename": filename,
        "row": row,
        "uploaded_at": datetime.datetime.utcnow()
    }
    db.images.insert_one(doc)
    return _format_image(doc)

def delete_image(db, image_id: str):
    try:
        obj_id = ObjectId(image_id)
    except Exception:
        return None
    doc = db.images.find_one({"_id": obj_id})
    if doc:
        db.images.delete_one({"_id": obj_id})
        return _format_image(doc)
    return None
