# diem.finance

Django-based financial management system with credit tracking, installment management, and analytics.

## Features

- Credit and transaction management
- Installment tracking and payment reminders
- Financial insights and analytics
- RESTful API with JWT authentication
- Celery-based scheduled tasks

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Cache/Queue**: Redis, Celery
- **Deployment**: Render

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables (see `.env.example`)
3. Run migrations: `python manage.py migrate`
4. Start development server: `python manage.py runserver`

## Production Deployment

The application is configured for deployment on Render with the included `build.sh` script.
