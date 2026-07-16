from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas, database
import os
import shutil
from .auth import get_current_admin

router = APIRouter(prefix="/images", tags=["images"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=schemas.Image)
def upload_image(file: UploadFile = File(...), db: Session = Depends(database.get_db), current_admin: models.Admin = Depends(get_current_admin)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    return crud.create_image(db=db, filename=file.filename)

@router.get("/", response_model=List[schemas.Image])
def read_images(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_images(db, skip=skip, limit=limit)

@router.delete("/{image_id}", response_model=schemas.Image)
def delete_image(image_id: int, db: Session = Depends(database.get_db), current_admin: models.Admin = Depends(get_current_admin)):
    image = crud.delete_image(db, image_id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    file_location = f"{UPLOAD_DIR}/{image.filename}"
    if os.path.exists(file_location):
        os.remove(file_location)
        
    return image
