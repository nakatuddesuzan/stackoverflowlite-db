import os
from configparser import ConfigParser


class BaseConfig(object):
    """
    Common configurations
    """
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/stackoverflow'


class TestingConfig(BaseConfig):
    """Configurations for Testing, with a separate test database."""
    DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/stackoverflow'
    TESTING = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    """
    Development configurations
    """

    DEBUG = True


class ProductionConfig(BaseConfig):
    """
    Production configurations
    """

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
