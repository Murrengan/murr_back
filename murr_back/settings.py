import datetime
import os
from datetime import timedelta

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SITE_ID = 1

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "+ownf%0op*r)rytn0^u38y7sbp_w6nf-uf9cbtm0sk2o#b1^bj")

DEBUG = bool(os.getenv("DJANGO_DEBUG", True))

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(" ")

ROOT_URLCONF = 'murr_back.urls'

WSGI_APPLICATION = 'murr_back.wsgi.application'

# WebSocket protocol
ASGI_APPLICATION = 'murr_back.routing.application'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
    'drf_yasg',
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
    'murr_search.apps.MurrSearchConfig',
]

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
]

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

BACKEND_URL = os.getenv("BACKEND_URL", 'http://127.0.0.1:8000')
FRONTEND_URL = os.getenv("FRONTEND_URL", 'http://127.0.0.1:8080')

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = f'/media/'
DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DJANGO_DB_ENGINE", 'django.db.backends.sqlite3'),
        "NAME": os.getenv("DJANGO_DB_DATABASE", os.path.join(BASE_DIR, 'db.sqlite3')),
        "USER": os.getenv("DJANGO_DB_USER"),
        "PASSWORD": os.getenv("DJANGO_DB_PASSWORD"),
        "HOST": os.getenv("DJANGO_DB_HOST"),
        "PORT": os.getenv("DJANGO_DB_PORT"),
    }
}

EMAIL_BACKEND = os.getenv("DJANGO_EMAIL_BACKEND", 'django.core.mail.backends.console.EmailBackend')
EMAIL_USE_TLS = bool(os.getenv("DJANGO_EMAIL_USE_TLS", False))
EMAIL_HOST = os.getenv("DJANGO_EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("DJANGO_EMAIL_HOST_USER")
EMAIL_PORT = os.getenv("DJANGO_EMAIL_PORT")
EMAIL_HOST_PASSWORD = os.getenv("DJANGO_EMAIL_HOST_PASSWORD")

AUTH_USER_MODEL = 'murren.Murren'

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

CORS_ALLOW_ALL_ORIGINS = bool(os.getenv("CORS_ALLOW_ALL_ORIGINS", False))
CORS_ORIGIN_WHITELIST = os.getenv("CORS_ORIGIN_WHITELIST", "http://127.0.0.1:8080 http://localhost:8080").split(" ")

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

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
]

DJOSER = {
    'ACTIVATION_URL': 'murren_email_activate/?murr_code=___{uid}___{token}___',
    'PASSWORD_RESET_CONFIRM_URL': 'set_new_password/?murr_code=___{uid}___{token}___',
    'SEND_ACTIVATION_EMAIL': True,
    'EMAIL': {
        'activation': 'murren.email.MurrenActivationEmail',
        'password_reset': 'murren.email.MurrenPasswordResetEmail',
    }
}

RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

if RECAPTCHA_SECRET_KEY:
    MIDDLEWARE.append('murr_back.middleware.CheckRecaptchaMiddleware')

RECAPTCHA_URL_PROTECTED = (
    'auth/users/reset_password_confirm/',
    'auth/users/',
    'auth/users/reset_password/',
    'api/murren/token_create/',
    'api/murr_card/',
    'api/murr_comments/'
)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(
                os.getenv("REDIS_HOST", "127.0.0.1"), 
                os.getenv("REDIS_PORT", 6379)
            )],
        },
    },
}

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

SENTRY_DSN = os.getenv("SENTRY_DSN")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR}/.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        }
    },
}
