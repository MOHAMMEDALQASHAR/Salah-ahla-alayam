import sys
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# Ensure backend directory is in sys.path for Vercel
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import auth, bookings, images, settings
import database

app = FastAPI(title="Ahla Al-Ayam Hall API")

# Setup CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(images.router)
app.include_router(settings.router)

# Serve uploaded images safely
uploads_dir = os.path.join(backend_dir, "uploads")
try:
    os.makedirs(uploads_dir, exist_ok=True)
except Exception:
    pass

if os.path.exists(uploads_dir):
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Serve Frontend static files
frontend_dir = os.path.join(backend_dir, "..", "frontend")
frontend_dir = os.path.abspath(frontend_dir)

if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def read_root():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(
            index_path,
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    return {"message": "Welcome to Ahla Al-Ayam Hall API. Frontend not found."}

@app.get("/admin")
def read_admin():
    admin_path = os.path.join(frontend_dir, "admin.html")
    if os.path.exists(admin_path):
        return FileResponse(
            admin_path,
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    return {"message": "Admin interface not found."}

@app.get("/health")
def health_check():
    """Check database connectivity"""
    try:
        db = database.get_db()
        # Ping the database
        db.command("ping")
        return {
            "status": "ok",
            "database": "connected",
            "uri_set": bool(os.getenv("MONGODB_URI")),
            "vercel": bool(os.environ.get("VERCEL"))
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "error": str(e),
            "uri_set": bool(os.getenv("MONGODB_URI")),
            "vercel": bool(os.environ.get("VERCEL"))
        }

