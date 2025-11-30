#!/bin/bash
# Script to initialize the database on container startup

set -e

echo "Waiting for database to be ready..."
sleep 5

echo "Initializing database..."
python init_db.py

echo "Seeding database with movies..."
python seed_db.py

echo "Database initialization complete!"
echo "🚀 Starting API server..."

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
