

from pathlib import Path
from datetime import timedelta
from .utils import get_connection_params
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pv_(wc#i9djlu+z65pk(vv)g%)z6&hr8$8sz=olr=ohw(2#b$z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'Authentications.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django_elasticsearch_dsl',
    'rest_framework',
    'corsheaders',
    'knox',
    'drf_yasg',
    # 'search.apps.SearchConfig',
    'Dashboard' ,
    'Authentications.apps.AuthenticationsConfig',
    'PreAuth.apps.PreauthConfig',
    'ClaimManagement.apps.ClaimmanagementConfig',
    'Query.apps.QueryConfig',
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

ROOT_URLCONF = 'ClaimAssurance.urls'

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

WSGI_APPLICATION = 'ClaimAssurance.wsgi.application'


config_path = "ClaimAssurance/db_info.ini"
section = "Postgres_DB_Info"

db_params = get_connection_params(config_path,section)

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':'CLAIMASSURE',
        'USER':'postgres',
        'PASSWORD':'admin',
        'HOST':'localhost',
        # 'HOST' : '10.202.100.7', 
        'PORT':'5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericpasswordValidator',
    # },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'Page_SIZE': 0,
    'DATETIME_INPUT_FORMATS': ["%d/%m/%Y %H:%M:%S %p" , "%d/%m/%Y %H:%M:%S"],
    'DATE_INPUT_FORMATS': ["%d/%m/%Y" , "%d-%m-%Y", "%Y-%m-%d"],

    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
} 

REST_KNOX = {
  'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
  'AUTH_TOKEN_CHARACTER_LENGTH': 64,
  'TOKEN_TTL': timedelta(hours=5), }



SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "api_key": {
            "name": "Authorization",
            "type": "apiKey",
            "in": "header",
        }
    },
    
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT", ]


# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3030',
# ]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/


LANGUage_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False

USE_L10N = True

TIME_ZONE = 'Asia/Kolkata'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

MEDIA_ROOT = BASE_DIR /"media"
MEDIA_URL = "/media/"
LOG_DIRECTORY = os.path.join(MEDIA_ROOT , 'logging')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



LOGGING = {
    "version":1,
    "disable_existing_loggers":False,
    "formatters":{
        "simple":{
            "format":"[%(asctime)s] : %(name)s - %(levelname)s - %(message)s",
            "datefmt":"%d %b %y %H:%M:%S"
        }
    },
    "handlers":{
        "console":{
            "level":"INFO",
            "class":"logging.StreamHandler",
            "formatter":"simple",
            "stream":"ext://sys.stdout"
        },
        "mail-handler":{
            "level":"ERROR",
            "class":"logging.handlers.SMTPHandler",
            "formatter":"simple",
            "mailhost":("smtp.gmail.com",587),
            "fromaddr":"",
            "toaddrs":[""],
            "subject":"Error occured in Claim-Assure....",
            "credentials":('jafarkhan301999@gmail.com', 'viqnqsrdvauymesk'),
            "secure":()
        },
        # "mail-handler":{
        #     "level":"ERROR",
        #     "class":"logging.handlers.SMTPHandler",
        #     "formatter":"simple",
        #     "mailhost":("Smtp.office365.com",587),
        #     "fromaddr":"your_mail",
        #     "toaddrs":["rcpt_mail"],
        #     "subject":"Error occured in NMSCDCL....",
        #     "credentials":('your_mail', 'your_password'),
        #     "secure":()
        # },
        "file-handler":{
            "level":"ERROR",
            "class":"logging.FileHandler",
            "formatter":"simple",
            "filename":"{}/error_log.log".format(LOG_DIRECTORY),
            "mode":"a"
        }
    },
    "loggers":{
        "django":{
            "level":"INFO",
            "handlers":["console"],
            "propagate":False
        },
        "claimAssure":{
            "level":"ERROR",
            "handlers":["mail-handler","file-handler"],
            "propagate":False
        }
    }
}




EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'jafarkhan301999@gmail.com'
EMAIL_HOST_PASSWORD = 'sgxddcxhtexkrgwv'
EMAIL_USE_TLS = True