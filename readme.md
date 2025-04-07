This project allows users to book appointments with doctors, pay for lab tests online, and securely share health records.

---

## 🚀 Getting Started

Follow these steps to set up and run the application locally.

### 1. Create Python Virtual Environment

#install django version specified in requirements.txt and Python 3.11.8

```bash

 1) Start python virtual env
    python -m venv venv
 2) Activate the virtual environment venv
    source venv/bin/activate
 3) Install python pip paclages
    pip install -r requirements
 4) Create .env from  .env.example and add secret key
    cp .env.example .env
 5) Upgrade django framework
    pip install --upgrade djangorestframework-simplejwt
 6) Migrate DB
    python manage.py migrate
 7) Start the application
    python manage.py runserver
```
