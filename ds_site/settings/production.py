"""
Django settings for ds_site project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

_file_dir = os.path.dirname(__file__)
_module_dir = os.path.split(_file_dir)[0]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3(bc&q3(nl*096$(6%-*cwxkiau&xn!zio*)8^-%pq$!pe!3#$'

# To use custom ERROR PAGES
# https://docs.djangoproject.com/en/1.10/topics/http/views/#customizing-error-views

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*'] # put in specific host when you know

ADMIN = (("Master", "philip.manno@gmail.com"),)

#  Email info, still testing
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'philip.manno@gmail.com'
EMAIL_HOST_PASSWORD = 'Zatoichi22'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # local apps
    'dsx',
    'common',
    'stage',
    'u',

    # third party apps
    'crispy_forms',
    'registration',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(_module_dir, 'templates'), # i think makes the templates folder in each module recognized; see code at top
        ],
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

WSGI_APPLICATION = 'ds_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# refer to link about to change DB settings in production
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'gc-newjack',
#         'USER': 'root',
#         'PASSWORD': 'Hellsing22',
#         'HOST': '',  # Set to empty string for localhost.
#         'PORT': '',  # Set to empty string for default.
#         #
#         # 'ENGINE': 'django.db.backends.sqlite3',
#         # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# [START db_setup]
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/newjack-steameng:us-central1:newjack-sql',
            'NAME': 'newjack',
            'USER': 'newjack-sql',
            'PASSWORD': 'Steameng1151',
        }
    }
else:
    # Running locally so connect to either a local MySQL instance or connect to
    # Cloud SQL via the proxy. To start the proxy via command line:
    #
    #     $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
    #
    # See https://cloud.google.com/sql/docs/mysql-connect-proxy
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'NAME': 'gc-newjack',
            'USER': 'root',
            'PASSWORD': 'Hellsing22',
        }
    }
# [END db_setup]



# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static") # where files are collected into; on production you have to change this to your webservers file structure path
#STATIC_ROOT = os.path.join(_module_dir, 'static/')

STATICFILES_DIRS = [                           # this is where your static files are being collected from
    os.path.join(BASE_DIR, "static_local"),
    #'/var/www/static/', # you can specify multiple sources
    ]

###this is where end user or staff files are going, repo for external people to upload files to your site
### There is no MEDIAFILES_DIRS because it is the user who is the source of the files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media") # where user files are uploaded; on production you have to change this to your webservers file structure path
#MEDIA_ROOT = os.path.join(_module_dir, 'media/') # might utilize this when you figure media uploads out

# Crispy Form Template Version
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Registration Redux Settings
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
SITE_ID = 1 # This is the index of the site registered in the 'Sites' Table in the admin
LOGIN_REDIRECT_URL = '/u/'