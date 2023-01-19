import contextlib
import json
import os
from strangler import get_strangler_log
from strangler.check import strangler_log_filename, STRANGLER_LOG_DIR


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


def raiser():
    raise RuntimeError()


def strangler_log_file_delete():
    with contextlib.suppress(FileNotFoundError):
        os.remove(strangler_log_filename())


def strangler_log_file_exists():
    return os.path.exists(strangler_log_filename())


def no_strangler_logging():
    return get_strangler_log() is None


def check_strangler_log(class_name, name, old_result, new_result):
    check_log(class_name, name, old_result, new_result)


def check_exc_log(exc, class_name, name, old_result, new_result):
    check_log(exc.info, class_name, name, old_result, new_result)


def check_log(class_name, name, old_result, new_result):
    log = get_strangler_log()
    diagnostic = json.dumps(log, indent=2)
    assert log["class"] == class_name, diagnostic
    assert log["name"] == name, diagnostic
    assert log["old-info"]["result"] == old_result, diagnostic
    assert log["new-info"]["result"] == new_result, diagnostic

