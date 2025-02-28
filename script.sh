#!/bin/bash
python manage.py ping &  
gunicorn library.wsgi:application