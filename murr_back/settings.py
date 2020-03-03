import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '+ownf%0op*r)rytn0^u38y7sbp_w6nf-uf9cbtm0sk2o#b1^bj'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'corsheaders',

    # if we want to add refresh token to blacklist
    # 'rest_framework_simplejwt.token_blacklist',

    # local
    'murren.apps.MurrenConfig',
    'murr_card.apps.MurrCardConfig',
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

    'murr_back.middleware.CheckRecaptchaMiddleware',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'murr_bd',
#         'USER': 'murr',
#         'PASSWORD': 'murr_password',
#         'HOST': '127.0.0.1',
#         'PORT': 5432,
#     }
# }

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
    "http://127.0.0.1:8080",

    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://35.230.139.201",
    "http://www.murrengan.ru",
]

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'murrengan.test@gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_PASSWORD = 'iufotejcfyojsgby'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {

    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    # 'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # 'ROTATE_REFRESH_TOKENS': True,

    # when we want to add refresh token to blacklist, uncomment this field and make migrations.
    # with this have some problem to remove murren form db
    # 'BLACKLIST_AFTER_ROTATION': True,
}

RECAPTCHA_URL_PROTECTED = (
    r'^murren/token_create/$',
    r'^murren/register/$',
    r'^murren/reset_password/$',
    r'^murren/confirm_new_password/$',
)
