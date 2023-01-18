import threading

_cc = threading.local()


def get_cc_log():  # pragma no cover
    if 'log' in _cc.__dict__:
        return _cc.log
    else:
        return None


def set_cc_log(log):
    _cc.log = log
