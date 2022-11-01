#!/bin/sh

echo "Starting to running app..."

gunicorn --bind :8000 --workers 3 run:app