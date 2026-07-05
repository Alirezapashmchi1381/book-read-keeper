#!/bin/sh
set -e

echo "Waiting for database..."

until python -c "
import socket
s = socket.socket()
s.connect(('db', 5432))
s.close()
"; do
    echo "Database is unavailable - sleeping"
    sleep 2
done

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting application..."
exec python3 main.py