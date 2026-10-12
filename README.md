# CodeAlpha_SocialMedia

Instagram-style social media platform built with Django.

## Features
- User authentication (register, login, logout)
- Profile with bio and picture
- Create posts (image upload / YouTube / Instagram)
- Like and comment system
- Responsive Bootstrap UI

## Tech Stack
- Django (Backend)
- Bootstrap 5 (Frontend)
- SQLite (Database)
- Cloudinary (Image storage)
- YouTube Data API v3

## Local Setup
1. Clone repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate`
4. Install: `pip install -r requirements.txt`
5. Create `.env` file (use `.env.example` as reference)
6. Migrate: `python manage.py migrate`
7. Run: `python manage.py runserver`

## Deploy
Deployed on Render with Cloudinary for media storage.