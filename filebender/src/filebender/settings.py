import os
here = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(here, '../../database/sqlite3.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = os.path.join(here, '../../media/')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&bhy2&*zy4wr%!yk7qv(yzb6*5s$h!mgs_nos!+@3^y0li31sb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'filebender.urls'

TEMPLATE_DIRS = (
    os.path.join(here, '../../templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
#    'django.contrib.admindocs',
    'filebender.files',
#    'djangosaml2',
)

#LOGIN_URL = '/saml2/login/'

#AUTHENTICATION_BACKENDS = (
#    'djangosaml2.backends.Saml2Backend',
#    'django.contrib.auth.backends.ModelBackend',
#)

SAML_CONFIG = { 
    'xmlsec_binary' : '/usr/bin/xmlsec1',
    "sp": {
          "name" : "Rolands SP",
          "url" : "http://www.example.com:8087/",
          "idp": {
              "urn:mace:example.com:saml:roland:idp": {
              "single_signon_service": "http://idp.example.com/sso"},
          },
    },
    
    "entityid" : "urn:mace:example.com:saml:roland:sp",
    "service": {
        "sp":{
            "name" : "Rolands SP",
            "url" : "http://www.example.com:8087/",
            "idp": {
                "urn:mace:example.com:saml:roland:idp": {
                    "single_signon_service": "http://idp.example.com/sso"},
            },
        }
    },
    "key_file" : "./mykey.pem",
    "cert_file" : "./mycert.pem",
    "attribute_map_dir": "./attributemaps",
    "organization": {
        "display_name":["Rolands identities"]
    },
    "contact_person": [{
        "givenname": "Roland",
        "surname": "Hedberg",
        "phone": "+46 90510",
        "mail": "roland@example.com",
        "type": "technical",
        }]
}

SAML_USERNAME_ATTRIBUTE = 'uid'
