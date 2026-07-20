import crud, schemas, database

def init_db():
    try:
        db = database.get_db()
        admin = crud.get_admin(db, username="admin")
        if not admin:
            admin_in = schemas.AdminCreate(username="admin", password="password")
            crud.create_admin(db, admin_in)
            print("Default admin created (admin / password)")
        else:
            print("Default admin already exists.")
        
        # Initialize default settings
        if not crud.get_setting(db, "daily_price"):
            crud.set_setting(db, "daily_price", "1000")
        if not crud.get_setting(db, "contact_phone"):
            crud.set_setting(db, "contact_phone", "+1234567890")
        if not crud.get_setting(db, "bank_name"):
            crud.set_setting(db, "bank_name", "مصرف الكريمي")
        if not crud.get_setting(db, "bank_account_name"):
            crud.set_setting(db, "bank_account_name", "قاعة أحلى الأيام")
        if not crud.get_setting(db, "bank_account_number"):
            crud.set_setting(db, "bank_account_number", "123456789")
        
        print("Database initialization complete.")
    except Exception as e:
        print(f"Database initialization error (Check MONGODB_URI): {e}")

if __name__ == "__main__":
    init_db()
