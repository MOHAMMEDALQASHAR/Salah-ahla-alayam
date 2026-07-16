import crud, schemas, database, models

def init_db():
    models.Base.metadata.create_all(bind=database.engine)
    db = database.SessionLocal()
    admin = crud.get_admin(db, username="admin")
    if not admin:
        admin_in = schemas.AdminCreate(username="admin", password="password")
        crud.create_admin(db, admin_in)
        print("Default admin created (admin / password)")
    
    # Initialize default settings
    if not crud.get_setting(db, "daily_price"):
        crud.set_setting(db, "daily_price", "1000")
    if not crud.get_setting(db, "contact_phone"):
        crud.set_setting(db, "contact_phone", "+1234567890")
    
    db.close()

if __name__ == "__main__":
    init_db()
