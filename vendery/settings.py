"""
Django settings for vendery project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9um+!0gl@dp46^aqqfn3ayfps*q)z#w%s6=7^4q5pc9#cy^%l='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.vendery.app','vendery.app','*', 'localhost']


# Application definition
SHARED_APPS = (
    'django_tenants',  # mandatory
    'vendery.customers', # you must list the app where your tenant model resides in

    'django.contrib.contenttypes',

    # everything below here is optional
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'jet',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_extensions',
    'widget_tweaks'

)

TENANT_APPS = (
    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.contenttypes',

    # your tenant-specific apps
    'vendery.inventory',
    # everything below here is optional
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'jet',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_extensions'
)

X_FRAME_OPTIONS='SAMEORIGIN' # only if django version >= 3.0

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PUBLIC_SCHEMA_URLCONF = 'vendery.public_urls'
ROOT_URLCONF = 'vendery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [f"{BASE_DIR}/templates"],  # -> Dirs used by the standard template loader
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            "loaders": [
                "django_tenants.template.loaders.filesystem.Loader",  # Must be first
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

MULTITENANT_TEMPLATE_DIRS = [
    f"{BASE_DIR}/vendery/tenants/%s/templates"
]

WSGI_APPLICATION = 'vendery.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'vendery',
        'USER': 'vendery',
        'PASSWORD': 'test1234',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'inventory.User'
APPEND_SLASH = True

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
import os

STATICFILES_FINDERS = [
    "django_tenants.staticfiles.finders.TenantFileSystemFinder",  # Must be first
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'compressor.finders.CompressorFinder',
]

MULTITENANT_STATICFILES_DIRS = [
    os.path.join(f"{BASE_DIR}/vendery", "tenants/%s/static"),
]


STATICFILES_STORAGE = "django_tenants.staticfiles.storage.TenantStaticFilesStorage"
REWRITE_STATIC_URLS = True

STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
MULTITENANT_RELATIVE_STATIC_ROOT = "tenants/%s"

TENANT_MODEL = "customers.Client" # app.Model
TENANT_DOMAIN_MODEL = "customers.Domain"  # app.Model
SITE_ID = 1


DEFAULT_FILE_STORAGE = "django_tenants.files.storage.TenantFileSystemStorage"

MEDIA_ROOT = f"{BASE_DIR}/vendery/apps_dir/media/"
MULTITENANT_RELATIVE_MEDIA_ROOT = "%s/other_dir"

JET_SIDE_MENU_COMPACT = True
JET_SIDE_MENU_ITEMS = [
    {'app_label': 'inventory', 'items': [
        {'name': 'category', 'label': 'Categorias'},
        {'name': 'clients', 'label': 'Clientes'},
        {'name': 'products', 'label': 'Productos'},
        {'name': 'tickets', 'label': 'Tickets'},
        {'name': 'vendors', 'label': 'Vendedores'},
        {'name': 'orders', 'label': 'Ventas'},
    ]},
    {'app_label': 'sites', 'items': [
        {'name': 'site', 'label': 'Páginas'},
    ]},
]
