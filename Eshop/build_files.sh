#!/bin/bash
echo "Building Project..."
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput
