import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@xo1n53t6=5i(z+u^-hb29q8ysmyj8hu$(3uo$y#5(v15_n&qc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'django_dragonpay_router'
]

MIDDLEWARE = []
ROOT_URLCONF = 'django_dragonpay_router.urls'
WSGI_APPLICATION = 'django_dragonpay_router.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Dragonpay Routing Configurations
DRAGONPAY_CALLBACK_URL = os.environ.get('DRAGONPAY_CALLBACK_URL')
if not DRAGONPAY_CALLBACK_URL:
    raise Exception('DRAGONPAY_CALLBACK_URL not set in environment!')

DRAGONPAY_CALLBACK_PAYOUT_URL = os.environ.get(
    'DRAGONPAY_CALLBACK_PAYOUT_URL',
    DRAGONPAY_CALLBACK_URL + 'payout/').replace('//', '/')

print '\033[92mCallback URL:', DRAGONPAY_CALLBACK_URL, '\033[0m'
print '\033[92mCallback Payout URL:', DRAGONPAY_CALLBACK_PAYOUT_URL, '\033[0m'

DRAGONPAY_ROUTES = {}

for key in os.environ.keys():
    _key = key.upper()
    if _key.startswith('DRAGONPAY_ROUTE_'):
        _key = key.replace('DRAGONPAY_ROUTE_', '').lower()
        val = os.environ[key]

        if not val.endswith('/'):
            val += '/'

        print '\033[94mAdding [%s]' % _key, val, 'to routes\033[0m'
        DRAGONPAY_ROUTES[_key] = val

if not DRAGONPAY_ROUTES:
    raise Exception('No dragonpay routes found in environment')

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s "
                      "[%(module)s.%(filename)s:%(funcName)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S %p"
        },
        'simple': {
            'format': '%(levelname)s %(module)s.%(filename)s:%(funcName)s:%(lineno)s > %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file-handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': "logs/django_dragonpay_router.log"
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django_dragonpay_router': {
            'handlers': ['console', 'file-handler'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
