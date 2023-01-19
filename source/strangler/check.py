from datetime import datetime
import json
import time
import traceback
from lib import LockedDir, in_unit_tests
from lib.diff import diff_only
from .switch import *
from .log import set_strangler_log


def strangled(cls, name, use, old, new):
    """
    cls: eg User
    name: eg "login_id"
    use: eg OLD_MAIN
    """
    class_name = cls.__name__
    primary, secondary = ps(class_name, use, old, new)
    p_res, p_exc, p_trace, p_repr, p_args, p_kwargs = call(class_name, name, primary)
    if secondary is not None:
        sync_check(class_name, name, use, p_res, p_exc, p_trace, p_repr, p_args, p_kwargs, secondary)
    return result_or_raise(p_res, p_exc)


def ps(class_name, use, old, new):
    # Select primary and/or secondary
    d = {
        OLD_ONLY: (old, None),
        NEW_TEST: (old, new if in_unit_tests() else None),
        OLD_MAIN: (old, new),
        NEW_MAIN: (new, old),
        NEW_ONLY: (new, None)
    }
    return d[use]


def call(class_name, name, func):
    f_res, f_exc, f_trace, f_repr, f_args, f_kwargs = "not-set", None, "", "not-set", None, None
    try:
        f_res = func()
    except Exception as exc:
        f_exc = exc
        f_trace = traceback.format_exc()
    try:
        f_repr = func._repr()
        f_args = func.args
        f_kwargs = func.kwargs
    except Exception:
        pass
    return f_res, f_exc, f_trace, f_repr, f_args, f_kwargs


def result_or_raise(res, exc):
    if exc is None:
        return res
    else:
        raise exc


def sync_check(class_name, name, use, p_res, p_exc, p_trace, p_repr, p_args, p_kwargs, secondary):
    s_res, s_exc, s_trace, s_repr, s_args, s_kwargs = call(class_name, name, secondary)
    # noinspection PyBroadException
    try:
        do_strangler_check(class_name, name, use,
                           p_res, p_exc, p_trace, p_repr, p_args, p_kwargs,
                           s_res, s_exc, s_trace, s_repr, s_args, s_kwargs)
    except StrangledDifference:
        raise
    except Exception:
        pass


def do_strangler_check(class_name, name, use,
                       p_res, p_exc, p_trace, p_repr, p_args, p_kwargs,
                       s_res, s_exc, s_trace, s_repr, s_args, s_kwargs):
    if p_exc is None and s_exc is None:  # neither raised
        if p_res == s_res:
            return                       # ok

    if p_exc is not None and s_exc is not None:
        return                           # both raised, ok

    now = datetime.utcfromtimestamp(time.time())
    p_info = info(p_res, p_exc, p_trace)
    s_info = info(s_res, s_exc, s_trace)
    old_res = p_res if old_is_primary(use) else s_res
    new_res = p_res if new_is_primary(use) else s_res
    diff = {
        "time": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "class": class_name,
        "name": name,
        "old-info": p_info if old_is_primary(use) else s_info,
        "old-repr": p_repr if old_is_primary(use) else s_repr,
        "old-args": p_args if old_is_primary(use) else s_args,
        "old-kwargs": p_kwargs if old_is_primary(use) else s_kwargs,
        "new-info": p_info if new_is_primary(use) else s_info,
        "new-repr": p_repr if new_is_primary(use) else s_repr,
        "new-args": p_args if new_is_primary(use) else s_args,
        "new-kwargs": p_kwargs if new_is_primary(use) else s_kwargs,
        "diff": diff_only(old_res, new_res)
    }

    if use is NEW_TEST:
        if in_unit_tests():
            raise StrangledDifference(diff)
        else:
            return
    else:
        log_difference(diff)


def old_is_primary(use):
    return use[2] == "old"


def new_is_primary(use):
    return use[2] == "new"


def info(res, exc, trace):
    return {
        "result": f"{res}",
        "exception": [f"{exc}"] + trace.split("\n")
    }


def log_difference(diff):
    set_strangler_log(diff)
    with LockedDir(STRANGLER_DEBUG_LOG_DIR):
        with open(STRANGLER_DEBUG_LOG_PATH, "a") as f:
            f.write(json.dumps(diff, indent=2))


class StrangledDifference(RuntimeError):

    def __init__(self, info):
        self.info = info

    def __str__(self):
        return json.dumps(self.info, indent=2)

    def __init__(self, info):
        self.info = info

    def __str__(self):
        return json.dumps(self.info, indent=2)


STRANGLER_DEBUG_LOG_DIR = "/tmp/strangler_debug_logs"
STRANGLER_DEBUG_LOG_PATH = f"{STRANGLER_DEBUG_LOG_DIR}/log"
