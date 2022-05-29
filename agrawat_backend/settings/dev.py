from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'insecure_zd0&536k68f%n3)t1+t(d@-44ehevjps-2)#@k7bsjc^'

ALLOWED_HOSTS = ['localhost', '127.0.0.1',
                 '.elasticbeanstalk.com']

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
)

CSRF_TRUSTED_ORIGINS = ['http://localhost:3000']

AWS_STORAGE_BUCKET_NAME = 'botdisco'

# Sentry Logging
# sentry_sdk.init(
#     dsn=os.getenv('SENTRY_DSN_URL'),
#     integrations=[DjangoIntegration()],

#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production,
#     traces_sample_rate=0.0,

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True,

#     # By default the SDK will try to use the SENTRY_RELEASE
#     # environment variable, or infer a git commit
#     # SHA as release, however you may want to set
#     # something more human-readable.
#     # release="myapp@1.0.0",

#     environment='dev'
# )

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
