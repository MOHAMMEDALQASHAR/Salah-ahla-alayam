import database

images = list(database.db.images.find())
print(f"Total images in DB: {len(images)}")
for img in images:
    print(f"  - {img.get('filename')}: row={img.get('row', 'MISSING')}")
