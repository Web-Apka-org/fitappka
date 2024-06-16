import sys
from datetime import timedelta
from pathlib import Path
from cryptography.hazmat.primitives import serialization

# load keys from files
PRIVATE_KEY: str = None
with open('main/keys/EdDSA', 'rb') as file:
    PRIVATE_KEY = serialization.load_ssh_private_key(
        file.read(),
        password=None
    )

if not PRIVATE_KEY:
    sys.exit(
        'Error:: Failed to load private key from main/keys/EdDSA. Aborting...'
    )

PUBLIC_KEY: str = None
with open('main/keys/EdDSA.pub', 'rb') as file:
    PUBLIC_KEY = serialization.load_ssh_public_key(
        file.read()
    )

if not PUBLIC_KEY:
    sys.exit(
        'Error:: Failed to load public key from main/keys/EdDSA.pub. Aborting...'
    )

# expire time for keys
JWT_TOKEN_EXPIRE = timedelta(days=7)
JWT_REFRESH_TOKEN_EXPIRE = timedelta(days=8)


AUTHENTICATION_BACKENDS = ['main.auth_backend.AuthBackend']

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-98*-u5_tptzspte%_d5-!$4wb)_)tdek5534k#p(!y7&*#t%ch'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'food',
    'recipies',
    'user_rating',
    'corsheaders',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = "account.User"

CORS_ALLOW_ALL_ORIGINS = False

LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'default': {
                'format': '({asctime}) {levelname}:: {message}',
                'style': '{',
            }
        },

        'handlers': {
            'console': {
                'level': 'NOTSET',
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            }
        },

        'root': {
            'handlers': ['console'],
            'level': 'NOTSET'
        },

        'loggers': {
            'fitappka.main': {
                'handlers': ['console']
            },
            'fitappka.account': {
                'handlers': ['console']
            },
            'fitappka.food': {
                'handlers': ['console']
            },
            'fitappka.plan': {
                'handlers': ['console']
            },
            'fitappka.recipies': {
                'handlers': ['console']
            },
            'fitappka.summary': {
                'handlers': ['console']
            },
            'fitappka.user_rating': {
                'handlers': ['console']
            },
            'fitappka.Token': {
                'handlers': ['console']
            }
        }
}
