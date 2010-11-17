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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(here, '../../database/sqlite3.db'),
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

SECRET_KEY = '&bhy2&*zy4wr%!yk7qv(yzb6*5s$h!mgs_nos!+@3^y0li31sb'

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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    
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
    'files',
    'djangosaml2',
    'debug_toolbar',
)

#LOGIN_URL = '/saml2/login/'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    'files.context_processors.auth_urls',
)
#AUTHENTICATION_BACKENDS = (
#    'djangosaml2.backends.Saml2Backend',
#    'django.contrib.auth.backends.ModelBackend',
#)

SAML_CONFIG = { 
    'xmlsec_binary' : '/opt/local/bin/xmlsec1',
    "sp": {
          "name" : "Gijs SP",
          "url" : "http://www.example.com:8087/",
          "idp": {
              "urn:mace:localhost:saml:gijs:idp": {
              "single_signon_service": "http://localhost:8002/simplesaml"},
          },
    },
    
    "entityid" : "urn:mace:localhost:saml:gijs:sp",
    "service": {
        "sp":{
            "name" : "Gijs SP",
            "url" : "http://localhost:8002/simplesaml",
            "idp": {
                "urn:mace:localhost:saml:gijs:idp": {
                    "single_signon_service": "http://localhost:8002/simplesaml"},
            },
            "endpoints": "",
        }
    },
 #   "key_file" : "./mykey.pem",
 #   "cert_file" : "./mycert.pem",
 #   "attribute_map_dir": "./attributemaps",
 #   "organization": {
 #       "display_name":["Rolands identities"]
 #   },
 #   "contact_person": [{
 #       "givenname": "Roland",
 #       "surname": "Hedberg",
 #       "phone": "+46 90510",
 #       "mail": "roland@example.com",
 #       "type": "technical",
 #       }]
}

SAML_USERNAME_ATTRIBUTE = 'uid'

INTERNAL_IPS = ('127.0.0.1',)

# where to store large upload
FILE_UPLOAD_TEMP_DIR='/tmp'
