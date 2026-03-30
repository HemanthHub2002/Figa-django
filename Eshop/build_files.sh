#!/bin/bash
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt
echo "Collecting static files... (from root)"
python3 manage.py collectstatic --noinput --clear
