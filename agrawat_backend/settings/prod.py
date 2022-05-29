import os
from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import ignore_logger

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['disco-prod-env.eba-3n23buip.us-east-1.elasticbeanstalk.com',
                 'api.botdisco.com', 'botdisco.com']

CORS_ORIGIN_WHITELIST = ('https://*.botdisco.com', 'https://www.dash.botdisco.com', 'https://dash.botdisco.com',
                         'https://botdisco.com', 'https://botdisco.netlify.app',)

CSRF_TRUSTED_ORIGINS = ['https://*.botdisco.com', 'https://www.dash.botdisco.com', 'https://dash.botdisco.com',
                        'https://botdisco.com', 'https://botdisco.netlify.app']

AWS_STORAGE_BUCKET_NAME = 'botdisco'

# Sentry Logging
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN_URL'),
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",

    environment='prod'
)
ignore_logger("django.security.DisallowedHost")

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# When you're ready to move to a Postgres Database, uncomment this block
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': '5432'
    }
}
