# API Employee & Attendance System

## Include
- Python 3.9+  
- PostgreSQL
- MySQL (jika tidak ada PostgreSQL)
- Framework: Django

## Fitur
- Authentication
- Manajemen Karyawan (CRUD)
- Absensi (Attendance)
- Laporan Absensi
- Server-Side Data Processing
- Export Data

## Setup Local
- python3 -m venv venv
- source venv/bin/activate
- cd eas
- pip install -r requirements.txt

## Migrasi
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser

## Run App
- python manage.py runserver