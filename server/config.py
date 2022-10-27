import os


def raise_(ex):  # pragma no cover
    raise ex


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or raise_(Exception('SECRET_KEY not set'))
