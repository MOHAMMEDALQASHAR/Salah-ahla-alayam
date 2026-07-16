from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas, database
from .auth import get_current_admin

router = APIRouter(prefix="/settings", tags=["settings"])

@router.get("/", response_model=List[schemas.Setting])
def read_settings(db: Session = Depends(database.get_db)):
    return crud.get_settings(db)

@router.get("/{key}", response_model=schemas.Setting)
def read_setting(key: str, db: Session = Depends(database.get_db)):
    setting = crud.get_setting(db, key=key)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting

@router.post("/", response_model=schemas.Setting)
def set_setting(setting: schemas.SettingCreate, db: Session = Depends(database.get_db), current_admin: models.Admin = Depends(get_current_admin)):
    return crud.set_setting(db=db, key=setting.key, value=setting.value)
