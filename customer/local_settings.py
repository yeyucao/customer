"""
Django settings for customer project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-f^grxd30qj3jh!7g3@#5_rnbx)bl2r48%4dpcll(a!#+y-#p9&"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bbs.apps.BbsConfig"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "bbs.middleware.auth.AuthMiddleware"
]

ROOT_URLCONF = "customer.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'templates')]   # 保证路径配置正确
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "customer.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangoblog',
        'USER': 'root',
        'PASSWORD': 'Heng1991!@#',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# LANGUAGE_CODE = "en-us"
LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "bbs/static")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ALI_PAY_APP_ID="2021005129640221"
ALI_PAY_DEBUG=True
ALI_PAY_CALL_BACK_URL="http://127.0.0.1:8000/index/pay_result/"
ALI_PAY_GATEWAY_URL="https://openapi.alipay.com/gateway.do?"

ALIPAY_PUBLIC_KEY_STRING = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA23YI/mG9AH2/ekR708NYnhbsao5yjTetNunB3uhfGE+b3Bh0n4EGqRByIFzei25lvG0OAdmkeu9Eq7pOrOVh5jcIR6bzLxrGXKKbF9TeBLdXyJ7aPzuzPJGweYjL2i+8zIInsUNpz/pecm3NWN6U7vnZofhaKEOE/ykH+4OcL4EfVf27aBq/jXI5ZQBu9lwnVA75gBS3B9Hf+UliVBg1T+Mn5F6fxmsuB6ktvjjO0b+Qe62rPuRXP9Q5bAyBZxldKC8sneBVImW/QacKMNBtHjHcc37tUiwa7vQQnpFMnZbOsU3abbvPOeYvk4tJJphi7L6tEV+7NCLtZPg/1tZJkQIDAQAB
-----END PUBLIC KEY-----"""
ALIPAY_PRIVATE_KEY_STRING = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAnXscWQxi6muzsG+2MA0TPiItGx+CzhW+rWlkU049ZYJSut6eWWl+eFca6ro4axAi501+Xwp4BnyepktOp34kWISUkHg3CCHR3yvpfgJzbO5YGF4Km01ox4DF8e1N/0g3zQdshcvQBAuQGqfPr7aeQ0I5qoS+Ge1pXxd1z8abgBDvDN2i3DuVTbMMzVPw1ez0bj1WKGMcxGwUVsT31Ct4DsVCm4H61Hms5M3Pj4m1kQpMnboM8NTGSrVgmdsMefLffvRTSALfSQJ7TzLugcjm5oqlKL7CLDpAzqXCpzVLSM27/dXAZoG4e70nkPRwvNQJ+c18DPaQNXoPTvE6a/9tmQIDAQABAoIBAA5Omvq0F2B4vHBxFboz1eW1MSffqwCSFSqoAodW+lj4iA+WHgi9ftHsB/P/SxTe+GzPK4Xy64ibVcaB3Pl2ilLIaL7fTRCeEfUWhjX+fwIMfVBpaslFNRm650DdcFKa+wbTf9Z/97wGWOczC7lI/APcRmTpfmPYn9QVy4w+3O27d5+qZY6/6ORp2MXJYt71AfbBosTAqjdC78lDS6yqOcvS47R7BM7wPms2ArTcPAVsbF1q2N6moLvO0Q7OpDzQ8Dxt7APOAuMfVDfEQiJZNWg5+AMXfL63PhdUOcOF6CKE6S1YLvVvzYQGfJ5oIkbQrSJp4q5QJbOPhYZtaOyEcQECgYEAy64MEIygjND3RJvnhyAXrCFVLUpGDG945RADI7Dwn+o74zekJwDA+WBVEXckbpUOVChQ/gFW/ZbQnuCbsVMaDmRjhxZybmD7GejqWD7S2r64C+lu7jXDjzDRT9J+0B1lNZeU7dr5l9rlu1767vJJEInp8NVO9R35QVtPrCdL+AkCgYEAxe8HAZ9B9dAdVSaU4x35tCUyDDcj5szyMZbxFZRmgjvlqbb9gNiT7I3Tjebozt4KKx15THEakzJScjJWh3YU4WIwz48fgMQpHjE0pBSNqbfjGVSo1lyfl3M/+nO6MYqkpZqQcEWWRnjw2UgK2R5uQUevuq1ByjpzFcH5H8VfjRECgYBmW342puVcPvu0oADXmFotJ8ctboELaM3Bl61sN1SFmOolwuWcsDVKXY4Cq/REGmZMBsLFE5lK8Yq//TJhB9k1WF/oGHDDZbtrBvEWDeRbB7NoURRtY9l2UVsvGSKfpdYh+55ddkkudlQzOIU0pc/wHs7RN/FpH3oOzTuZ0VnNOQKBgQCVFdQuKZmSIB5n67aLVyGkybtnrgSxrD7kkS+ntG59u8Xhzj4lVXwd2jm1kW5bmq0ICpw5spt0sZud/kJkp9FUbhQb0k7FO3tJDYD78as+YY6Bnt3JEFz4w0s2RwLAnBAl2ETg+9kT3bZzwqrBHQWoz+kR77w1KU9T3RXbE1xEMQKBgAM/p82xsSpO50gxqrSo0NAY1W68zOmYzsFszc/ncaECDaq5lmLA+BHj9qJgtA8mnHcBlXmlrO58kV30Tv72MVaB0Rtw/Am6MaS0xTPqhrBj4WbQbTW0CZnl63J/vwRrD7tu/G5L/djqKkBYnhherWoMPuv7iY39ep0pKete2nrj
-----END RSA PRIVATE KEY-----"""

FILE_DOWN_PATH = os.path.dirname(os.path.abspath(__file__))