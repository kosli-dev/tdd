import json
import os
from strangler import get_cc_log


class ScopedEnvVar(object):

    def __init__(self, name, value):
        self.__name = name
        self.__old_value = os.environ.get(name)
        self.__new_value = value

    def __enter__(self):
        os.environ[self.__name] = self.__new_value

    def __exit__(self, _type, _value, _traceback):
        if self.__old_value is None:
            os.environ.pop(self.__name)
        else:
            os.environ[self.__name] = self.__old_value


def raiser(s=None):
    if s is None:
        s = "xyzzy"
    raise RuntimeError(s)


def no_cc_logging():
    return get_cc_log() is None


def check_cc_log(class_name, name, c_result, m_result):
    check_log(get_cc_log(), class_name, name, c_result, m_result)


def check_exc_log(exc, class_name, name, c_result, m_result):
    check_log(exc.info, class_name, name, c_result, m_result)


def check_log(log, class_name, name, c_result, m_result):
    diagnostic = json.dumps(log, indent=2)
    assert log["class"] == class_name, diagnostic
    assert log["name"] == name, diagnostic
    assert log["overwrite-db"]["result"] == c_result, diagnostic
    assert log["append-db"]["result"] == m_result, diagnostic

