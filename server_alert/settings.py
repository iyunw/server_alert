"""
Django settings for server_alert project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, "apps"))

load_dotenv()
# ENABLE_MYSQL = os.environ.get('ENABLE_MYSQL', "").lower() in ["1", "true", "yes"]
MYSQL_DB_HOST = os.environ.get('MYSQL_DB_HOST', "127.0.0.1")
MYSQL_DB_NAME = os.environ.get('MYSQL_DB_NAME', None)
MYSQL_USER_NAME = os.environ.get('MYSQL_USER_NAME', None)
MYSQL_USER_PASSWORD = os.environ.get('MYSQL_USER_PASSWORD', None)
MYSQL_PORT = os.environ.get('MYSQL_PORT', 3306)
EMAIL_HOST = os.environ.get('EMAIL_HOST', "")
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', "")
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', "")
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', "")
EMAIL_PORT = os.environ.get('EMAIL_PORT', "")
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', "").lower() in ["1", "true", "yes"]
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', "").lower() in ["1", "true", "yes"]
BASE_URL = os.environ.get('BASE_URL', "")
FONT_URL = os.environ.get('FONT_URL', "")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n42+k!)66-+)$f+w#h^8vqk3j1u&70yq!ogd4i7ny1oo3qc^aa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'user',
    'alert',
    'rest_framework',
    'rest_framework.authtoken'
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

ROOT_URLCONF = 'server_alert.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'server_alert.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': MYSQL_DB_HOST,
        'NAME': MYSQL_DB_NAME,
        'USER': MYSQL_USER_NAME,
        'PASSWORD': MYSQL_USER_PASSWORD,
        'PORT': MYSQL_PORT
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "user.User"

#配置全局rest framework设置
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
            # 'rest_framework.permissions.IsAuthenticated', #只允许登录才能访问
           'utils.drf.permission.IsActiveAuthenticated',  # 只允许登录才能访问
        ], #权限设置
    'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ) #认证方式，主要SessionAuthentication认证需要开启，不然api的URL无法登录

}


# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

########## EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_USE_SSL = EMAIL_USE_SSL

#### URL 服务端地址
BASE_URL = BASE_URL
FONT_URL = FONT_URL


