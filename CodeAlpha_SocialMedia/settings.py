"""
Django settings for CodeAlpha_SocialMedia project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────
# BASE DIRECTORY
# ─────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')


# ─────────────────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────────────────
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-change-me')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']  # Render deployment-ku


# ─────────────────────────────────────────────────────────
# APPLICATIONS
# ─────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'cloudinary_storage',       # Must come BEFORE cloudinary
    'cloudinary',

    # Local apps
    'social_app',
]


# ─────────────────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files serve
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ─────────────────────────────────────────────────────────
# URLS & TEMPLATES
# ─────────────────────────────────────────────────────────
ROOT_URLCONF = 'CodeAlpha_SocialMedia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CodeAlpha_SocialMedia.wsgi.application'


# ─────────────────────────────────────────────────────────
# DATABASE (SQLite)
# ─────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ─────────────────────────────────────────────────────────
# PASSWORD VALIDATION
# ─────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─────────────────────────────────────────────────────────
# INTERNATIONALIZATION
# ─────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # India time
USE_I18N = True
USE_TZ = True


# ─────────────────────────────────────────────────────────
# STATIC FILES (CSS, JS)
# ─────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'         # collectstatic-ku (Render)
STATICFILES_DIRS = [BASE_DIR / 'static']       # Dev-ku

# Whitenoise compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ─────────────────────────────────────────────────────────
# MEDIA FILES (Image upload)
# ─────────────────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Local dev-ku


# ─────────────────────────────────────────────────────────
# CLOUDINARY (Production-ku image storage)
# ─────────────────────────────────────────────────────────
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# Use Cloudinary in production (DEBUG=False), local storage in dev
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


# ─────────────────────────────────────────────────────────
# YOUTUBE API
# ─────────────────────────────────────────────────────────
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/search'


# ─────────────────────────────────────────────────────────
# AUTHENTICATION REDIRECTS
# ─────────────────────────────────────────────────────────
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'


# ─────────────────────────────────────────────────────────
# FILE UPLOAD LIMITS (5 MB max for images)
# ─────────────────────────────────────────────────────────
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880      # 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880      # 5 MB


# ─────────────────────────────────────────────────────────
# DEFAULT PRIMARY KEY
# ─────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ─────────────────────────────────────────────────────────
# MESSAGES FRAMEWORK (Bootstrap alert classes)
# ─────────────────────────────────────────────────────────
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}