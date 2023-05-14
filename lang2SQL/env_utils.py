import os


def is_production():
    return os.environ.get('ENVIRONMENT') == 'production'
