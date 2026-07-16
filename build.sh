#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r backend/requirements.txt

# Initialize database with default admin
cd backend
python init_db.py
