
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in {'1', 'true', 'yes', 'on'}


SECRET_KEY = 'django-insecure-o97f^!jim!$2k+oce&wnw3^esn3rl+g*q!u5x5paf5#ynwjdpc'

DEBUG = True

ALLOWED_HOSTS = ['*']



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fitness',
    'site_app',
]

try:
    import cloudinary  # noqa: F401
    import cloudinary_storage  # noqa: F401
except ImportError:
    CLOUDINARY_PACKAGES_AVAILABLE = False
else:
    CLOUDINARY_PACKAGES_AVAILABLE = True
    INSTALLED_APPS += [
        'cloudinary_storage',
        'cloudinary',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'fitness.middleware.SiteSettingsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ScaleFit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'fitness' / 'templates', BASE_DIR / 'site_app' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'fitness.context_processors.active_site_theme',
                'fitness.context_processors.current_user_profile',
                'fitness.context_processors.global_site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'ScaleFit.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



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



LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('ta', _('Tamil')),
    ('hi', _('Hindi')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'fitness' / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cloudinary keeps uploaded media out of SQLite and the local filesystem.
# Existing local files continue to resolve through MEDIA_URL; when Cloudinary
# credentials are present, new uploads are stored remotely by the hybrid storage
# backend in fitness.media_storage.
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', '')
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
    'SECURE': env_bool('CLOUDINARY_SECURE', True),
}
CLOUDINARY_CONFIGURED = bool(
    CLOUDINARY_URL or all(CLOUDINARY_STORAGE[key] for key in ('CLOUD_NAME', 'API_KEY', 'API_SECRET'))
)
USE_CLOUDINARY_STORAGE = (
    CLOUDINARY_PACKAGES_AVAILABLE
    and CLOUDINARY_CONFIGURED
    and env_bool('USE_CLOUDINARY_STORAGE', True)
)

if USE_CLOUDINARY_STORAGE:
    STORAGES = {
        'default': {
            'BACKEND': 'fitness.media_storage.ScaleFitCloudinaryMediaStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
    DEFAULT_FILE_STORAGE = 'fitness.media_storage.ScaleFitCloudinaryMediaStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
