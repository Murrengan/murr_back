import datetime
import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY", '+ownf%0op*r)rytn0^u38y7sbp_w6nf-uf9cbtm0sk2o#b1^bj')

DEBUG = int(os.environ.get("DEBUG", default=1))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", '*').split(" ")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 3rd party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djoser',
    'channels',
    'mptt',
    'django_filters',

    # if we want to add refresh token to blacklist
    # 'rest_framework_simplejwt.token_blacklist',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # local
    'murren.apps.MurrenConfig',
    'murr_card.apps.MurrCardConfig',
    'murr_chat.apps.MurrChatConfig',
    'murr_bot.apps.MurrBotConfig',
    'murr_comments.apps.MurrCommentsConfig',
    'murr_rating.apps.MurrRatingConfig',
]

SITE_ID = 1

MIDDLEWARE = [
    # 3rd party
    'corsheaders.middleware.CorsMiddleware',

    # local
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'murr_back.middleware.CheckRecaptchaMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'murr_back.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'murr_back.wsgi.application'
ASGI_APPLICATION = 'murr_back.routing.application'

BASE_URL = os.environ.get("BASE_URL", 'http://127.0.0.1:8080')
LOCALHOST = os.environ.get("LOCALHOST", 'http://127.0.0.1:8000')

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", 'django.db.backends.sqlite3'),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, 'db.sqlite3')),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

AUTH_USER_MODEL = 'murren.Murren'

CORS_ORIGIN_WHITELIST = [
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
    "http://www.murrengan.ru",
    "https://www.murrengan.ru",
]

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", 'django.core.mail.backends.console.EmailBackend')
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'PAGE_SIZE': 30
}

REST_USE_JWT = True

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=14),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

RECAPTCHA_URL_PROTECTED = (
    'auth/users/reset_password_confirm/',
    'auth/users/',
    'auth/users/reset_password/',
    'api/murren/token_create/',
    'api/murr_card/'
)

DJOSER = {
    'ACTIVATION_URL': 'murren_email_activate/?murr_code=___{uid}___{token}___',
    'PASSWORD_RESET_CONFIRM_URL': 'set_new_password/?murr_code=___{uid}___{token}___',
    'SEND_ACTIVATION_EMAIL': True,
    'EMAIL': {
        'activation': 'murren.email.MurrenActivationEmail',
        'password_reset': 'murren.email.MurrenPasswordResetEmail',
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
