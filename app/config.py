from instance.config import SECRET_KEY
import os
class Config:
    """
    General configurations parent class
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://pato:flower2@localhost/watchlist'
class ProdConfig(Config):
    """
    Production configuration child class
    Args:
    Config:The parent configuration class with parent config settings
    """
    pass


class DevConfig(Config):
    """
    Development configuration child class
    Args:
    Config: Parent configuration class 
    """
    DEBUG = True


config_options = {
    'development':DevConfig,
    'production':ProdConfig
    }   
