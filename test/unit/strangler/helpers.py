import contextlib
import json
import os
from strangler import strangler_log_filename, OLD_ONLY, OLD_MAIN, NEW_ONLY, NEW_MAIN


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
    return not strangler_log_file_exists()


def check_strangler_exc(exc, call, old_result, new_result):
    log = exc.value.diff
    diagnostic = json.dumps(log, indent=2)
    assert log["call"] == call, diagnostic
    assert log["old"]["result"] == old_result, diagnostic
    assert log["new"]["result"] == new_result, diagnostic

