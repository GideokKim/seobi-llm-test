import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't') 