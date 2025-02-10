"""
Django settings for paleo_project project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g7zcfmg3p8)d&*0&@2utf$!tw^f&8dth9^sqtj1id!cecosx58'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'rest_framework',
    'drf_yasg',
    "corsheaders"
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'paleo_project.urls'

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

WSGI_APPLICATION = 'paleo_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'paleo_project',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5434'
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AWS_STORAGE_BUCKET_NAME = 'paleoproject'
AWS_ACCESS_KEY_ID = '55zrhuUGuiNEjHA3zZgC'
AWS_SECRET_ACCESS_KEY = 'tTYfK1VGaLaKAgTeNcTgrxD7NURrYAzomGZl4jX4'
AWS_S3_ENDPOINT_URL = 'localhost:9000'
MINIO_USE_SSL = False


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ]
}

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

# # CORS_ORIGIN_ALLOW_ALL = True
# # CORS_ALLOW_ALL_ORIGINS = True
# # CORS_ALLOW_CREDENTIALS = True
# # CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:8000"]
# CORS_ALLOW_HEADERS = ["*"]
# # CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
# # CORS_ALLOW_ALL_METHODS = True

# CORS_ALLOWED_ORIGINS = ["http://localhost:3000",]
# CORS_ALLOW_CREDENTIALS = True

# CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]
# CSRF_COOKIE_HTTPONLY = False




CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
	"http://127.0.0.1:3000",
	"http://192.168.31.8:3000",
	"http://172.20.10.2:3000",
    "http://192.168.0.13:8081"
]

CORS_ALLOW_CREDENTIALS = True







# SECURE_CROSS_ORIGIN_OPENER_POLICY = None

# CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,  # Отключаем авторизацию через сессию Django
    "SECURITY_DEFINITIONS": {
        "apiKey": {
            "type": "apiKey",
            "in": "cookie",  # Передавать куку
            "name": "session_id",  # Имя куки (должно совпадать с тем, что ты устанавливаешь в set_cookie)
        }
    },
    "PERSIST_AUTH": True,  # Сохранение аутентификации между запросами
}


HOST = "192.168.0.13"
