import contextlib
import json
import os
from strangler import get_strangler_log
from strangler.strangled import strangler_log_filename


class ScopedEnvVar(object):

    def __init__(self, name, value):
        self.name = name
        self.old_value = os.environ.get(name)
        self.new_value = value

    def __enter__(self):
        os.environ[self.name] = self.new_value

    def __exit__(self, _type, _value, _traceback):
        if self.old_value is None:
            os.environ.pop(self.name)
        else:
            os.environ[self.name] = self.old_value


def raiser(exc):
    raise exc


def strangler_log_file_delete():
    with contextlib.suppress(FileNotFoundError):
        os.remove(strangler_log_filename())


def strangler_log_file_exists():
    return os.path.exists(strangler_log_filename())


def no_strangler_logging():
    return get_strangler_log() is None


#def check_strangler_log(class_name, name, old_result, new_result):
#    _check_log(get_strangler_log(), class_name, name, old_result, new_result)


def check_strangler_exc(exc, class_name, name, old_result, new_result):
    _check_log(exc.value.diff, class_name, name, old_result, new_result)


def _check_log(log, class_name, name, old_result, new_result):
    diagnostic = json.dumps(log, indent=2)
    assert log["class"] == class_name, diagnostic
    assert log["name"] == name, diagnostic
    assert log["old"]["result"] == old_result, diagnostic
    assert log["new"]["result"] == new_result, diagnostic

