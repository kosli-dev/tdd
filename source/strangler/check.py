from datetime import datetime
import json
import os
import time
import traceback
from lib import LockedDir, i_am_doing_the_migration, in_unit_tests
from lib.diff import diff_only
from .switch import *
from .log import set_cc_log


def strangled(cls, name, kind, use, c, m):
    """
    cls: eg User
    name: eg "login_id"
    kind: eg "query"
    use: eg OLD_MAIN
    """
    class_name = cls.__name__
    primary, secondary = ps(class_name, kind, use, c, m)
    p_res, p_exc, p_trace, p_repr, p_args, p_kwargs = call(class_name, kind, name, primary)
    if secondary is not None:
        sync_check(class_name, name, kind, use, p_res, p_exc, p_trace, p_repr, p_args, p_kwargs, secondary)
    return result_or_raise(p_res, p_exc)


def ps(class_name, kind, use, ow, ao):
    # Select primary and/or secondary
    if class_is_in_migration(class_name):
        if i_am_doing_the_migration():
            if kind == "query":
                return ow, None  # migrator must read from overwrite only
            else:
                return None, ao  # migrator must write to append only
        else:
            return ow, None  # server must not use Mongo

    d = {
        OLD_ONLY: (ow, None),
        NEW_TEST: (ow, ao if in_unit_tests() else None),
        OLD_MAIN: (ow, ao),
        NEW_MAIN: (ao, ow),
        NEW_ONLY: (ao, None)
    }
    return d[use]


def class_is_in_migration(class_name):
    filename = migration_marker_filename(class_name)
    return os.path.exists(filename)


def migration_marker_filename(class_name):
    return f"/tmp/{class_name}.migration.marker"


def call(class_name, kind, name, func):
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


def sync_check(class_name, name, kind, use, p_res, p_exc, p_trace, p_repr, p_args, p_kwargs, secondary):
    s_res, s_exc, s_trace, s_repr, s_args, s_kwargs = call(class_name, kind, name, secondary)
    # noinspection PyBroadException
    try:
        do_contract_check(class_name, name, kind, use,
                          p_res, p_exc, p_trace, p_repr, p_args, p_kwargs,
                          s_res, s_exc, s_trace, s_repr, s_args, s_kwargs)
    except StranglerDifference:
        raise
    except Exception:
        pass


def do_contract_check(class_name, name, kind, use,
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
    ow_res = p_res if old_is_primary(use) else s_res
    ao_res = p_res if new_is_primary(use) else s_res
    diff = {
        "time": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "class": class_name,
        "name": name,
        "kind": kind,
        "old-db": p_info if old_is_primary(use) else s_info,
        "old-repr": p_repr if old_is_primary(use) else s_repr,
        "old-args": p_args if old_is_primary(use) else s_args,
        "old-kwargs": p_kwargs if old_is_primary(use) else s_kwargs,
        "new-db": p_info if new_is_primary(use) else s_info,
        "new-repr": p_repr if new_is_primary(use) else s_repr,
        "new-args": p_args if new_is_primary(use) else s_args,
        "new-kwargs": p_kwargs if new_is_primary(use) else s_kwargs,
        "diff": diff_only(ow_res, ao_res)
    }

    if use is NEW_TEST:
        if in_unit_tests():
            raise StranglerDifference(diff)
        else:
            return
    else:
        log_difference(kind, diff)


def old_is_primary(use):
    return use[2] == "old"


def new_is_primary(use):
    return use[2] == "new"


def info(res, exc, trace):
    return {
        "result": f"{res}",
        "exception": [f"{exc}"] + trace.split("\n")
    }


def log_difference(kind, diff):
    set_cc_log(diff)
    with LockedDir(STRANGLER_DEBUG_LOG_DIR):
        if kind == "query":
            with open(STRANGLER_DEBUG_LOG_QUERY_PATH, "a") as f:
                f.write(json.dumps(diff, indent=2))
        if kind == "command":
            with open(STRANGLER_DEBUG_LOG_COMMAND_PATH, "a") as f:
                f.write(json.dumps(diff, indent=2))
        if kind == "create":
            with open(STRANGLER_DEBUG_LOG_CREATE_PATH, "a") as f:
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
STRANGLER_DEBUG_LOG_QUERY_PATH = f"{STRANGLER_DEBUG_LOG_DIR}/query.log"
STRANGLER_DEBUG_LOG_COMMAND_PATH = f"{STRANGLER_DEBUG_LOG_DIR}/command.log"
STRANGLER_DEBUG_LOG_CREATE_PATH = f"{STRANGLER_DEBUG_LOG_DIR}/create.log"
