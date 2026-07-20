from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List
import crud, schemas, database
import os
import shutil
from .auth import get_current_admin

router = APIRouter(prefix="/images", tags=["images"])

UPLOAD_DIR = "/tmp/uploads" if os.environ.get("VERCEL") else "uploads"
try:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
except Exception:
    pass

@router.post("/", response_model=schemas.Image)
def upload_image(file: UploadFile = File(...), row: str = Form("top"), db = Depends(database.get_db), current_admin = Depends(get_current_admin)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    return crud.create_image(db=db, filename=file.filename, row=row)

@router.get("/", response_model=List[schemas.Image])
def read_images(skip: int = 0, limit: int = 100, db = Depends(database.get_db)):
    return crud.get_images(db, skip=skip, limit=limit)

@router.delete("/{image_id}", response_model=schemas.Image)
def delete_image(image_id: str, db = Depends(database.get_db), current_admin = Depends(get_current_admin)):
    image = crud.delete_image(db, image_id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    file_location = f"{UPLOAD_DIR}/{image['filename']}"
    if os.path.exists(file_location):
        os.remove(file_location)
        
    return image
