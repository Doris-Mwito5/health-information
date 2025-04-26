# Health Information System

[![Django](https://img.shields.io/badge/Django-4.2-green)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A Django-based system for managing clients and health programs with REST API support.

## ✅ Features

1. **User Management**
   - Doctor/staff authentication
   - Token-based API authentication

2. **Health Programs**
   - Create/view/update programs (TB, Malaria, HIV)
   - Program enrollment tracking

3. **Client Management**
   - Patient registration
   - Profile management
   - Program enrollment

4. **Search & Reporting**
   - Client search functionality
   - Enrollment reports

5. **REST API**
   - Client/program endpoints

## 🎥 Demo Video

[![Demo Video](https://img.shields.io/badge/Demo-Video-blue)](https://drive.google.com/file/d/1kaZ4FZMoKxcZTHbJuVFSG2GfuLU4hFQU/view?usp=sharing)

## 🛠️ Installation

```bash
# Clone repository
git clone https://github.com/Doris-Mwito5/health-information.git
cd health-information

# Setup environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Configure and run
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
