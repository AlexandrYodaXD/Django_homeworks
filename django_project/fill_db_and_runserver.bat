@echo off
del db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py fill_db 10 20 30
python manage.py runserver