import os


def raise_(ex):  # pragma no cover
    raise ex


def wtf_csrf_enabled():
    env_var = os.environ.get('WTF_CSRF_ENABLED', True)
    if env_var == 'False':  # pragma no cover
        env_var = False
    return env_var


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or raise_(Exception('SECRET_KEY not set'))

    WTF_CSRF_ENABLED = wtf_csrf_enabled()
