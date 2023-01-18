import threading

_strangler = threading.local()


def get_strangler_log():  # pragma no cover
    if 'log' in _strangler.__dict__:
        return _strangler.log
    else:
        return None


def set_strangler_log(log):
    _strangler.log = log
