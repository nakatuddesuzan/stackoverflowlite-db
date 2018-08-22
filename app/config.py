import os
from configparser import ConfigParser


class BaseConfig(object):
    """
    Common configurations
    """
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.urandom(24)


class TestingConfig(BaseConfig):
    """Configurations for Testing, with a separate test database."""
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

def config(filename = 'database.ini', section = 'postgresql'):
    #create parser
    parser = ConfigParser()
    #read the config file
    parser.read(filename)

    #get section default to postgresql
    db ={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in  params:
            db[param[0]] = param[1]
    else:
        raise Exception('section {0} not found in the {1} file' .format(section, filename))
    return db