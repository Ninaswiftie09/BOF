# proyecto_django/settings_test.py

from .settings import *

from decouple import Config, RepositoryEnv
import os

ENV_TEST_PATH = os.path.join(BASE_DIR, '.env.test')
config_test = Config(RepositoryEnv(ENV_TEST_PATH))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config_test("DB_NAME"),
        'USER': config_test("DB_USER"),
        'PASSWORD': config_test("DB_PASSWORD"),
        'HOST': config_test("DB_HOST"),
        'PORT': config_test("DB_PORT"),
    }
}
