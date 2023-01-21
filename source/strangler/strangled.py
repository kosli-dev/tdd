from datetime import datetime
import json
import threading
import time
import traceback
from .in_unit_tests import in_unit_tests
# from lib.diff import diff_only
from .switch import *
from .log import set_strangler_log


def strangled(cls, name, use, old, new):
    """
    cls: eg User
    name: eg "login_id"
    use: eg OLD_MAIN
    """
    class_name = cls.__name__
    primary, secondary = ps(use, old, new)
    p_res, p_exc, p_trace, p_repr, p_args, p_kwargs = call(primary)
    if secondary is not None:
        s_res, s_exc, s_trace, s_repr, s_args, s_kwargs = call(secondary)
        strangled_check(class_name, name, use,
                        p_res, p_exc, p_trace, p_repr, p_args, p_kwargs,
                        s_res, s_exc, s_trace, s_repr, s_args, s_kwargs)
    if p_exc is None:
        return p_res
    else:
        raise p_exc


def ps(use, old, new):
    # Select primary and/or secondary
    d = {
        OLD_ONLY: (old, None),
        NEW_TEST: (old, new),  # See [1]
        OLD_MAIN: (old, new),
        NEW_MAIN: (new, old),
        NEW_ONLY: (new, None)
    }
    return d[use]


def call(func):
    f_res = "not-set"
    f_exc = None
    f_trace = ""
    f_repr = "not-set"
    try:
        f_res = func()
    except Exception as exc:
        f_exc = exc
        f_trace = traceback.format_exc()

    f_args = func.args
    f_kwargs = func.kwargs
    # noinspection PyBroadException
    try:
        f_repr = repr(func)
    except Exception:
        pass

    return f_res, f_exc, f_trace, f_repr, f_args, f_kwargs


def strangled_check(class_name, name, use,
                    p_res, p_exc, p_trace, p_repr, p_args, p_kwargs,
                    s_res, s_exc, s_trace, s_repr, s_args, s_kwargs):
    diagnostic = None
    neither_raised = p_exc is None and s_exc is None
    both_raised = p_exc is not None and s_exc is not None

    if neither_raised:
        try:
            if p_res == s_res:
                return
        except Exception as exc:
            diagnostic = "\n".join([
                "'if p_res == s_res:' raised...",
                str(exc)
            ])
    elif both_raised:
        if type(p_exc) is type(s_exc):
            return
        else:
            diagnostic = "\n".join([
                "type(p_exc) != type(s_exc)",
                f"type(p_exc) is {type(p_exc).__name__}",
                f"type(s_exc) is {type(s_exc).__name__}"
            ])
    else:
        def primary():
            return "old" if old_is_primary(use) else "new"

        def secondary():
            return "old" if new_is_primary(use) else "old"

        def raised(ex):
            return "raised" if ex is not None else "did not raise"
        diagnostic = f"{primary()} {raised(p_exc)}, {secondary()} {raised(s_exc)}"

    def old(p, s):
        return p if old_is_primary(use) else s

    def new(p, s):
        return p if new_is_primary(use) else s

    now = datetime.utcfromtimestamp(time.time())
    # old_res = old(p_res, s_res)
    # new_res = new(p_res, s_res)
    diff = {
        "time": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "class": class_name,
        "name": name,
        "diagnostic": diagnostic,
        # "diff": diff_only(old_res, new_res)
        "old": {
            "is": old("primary", "secondary"),
            "repr": old(p_repr, s_repr),
            "args": old(p_args, s_args),
            "kwargs": old(p_kwargs, s_kwargs),
            "result": f"{old(p_res, s_res)}",
            "exception": f"{old(p_exc, s_exc)}",
            "trace": old(p_trace, s_trace).split("\n")
        },
        "new": {
            "is": new("primary", "secondary"),
            "repr": new(p_repr, s_repr),
            "args": new(p_args, s_args),
            "kwargs": new(p_kwargs, s_kwargs),
            "result": f"{new(p_res, s_res)}",
            "exception": f"{new(p_exc, s_exc)}",
            "trace": new(p_trace, s_trace).split("\n")
        }
    }

    if use is NEW_TEST:  # [1]
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


def log_difference(diff):
    set_strangler_log(diff)
    with open(strangler_log_filename(), "a") as f:
        f.write(json.dumps(diff, indent=2))


def strangler_log_filename():
    tid = threading.get_ident()
    return f"/tmp/strangler_logs/log.{tid}"


class StrangledDifference(RuntimeError):

    def __init__(self, diff):
        self.diff = diff

    def __str__(self):
        return json.dumps(self.info, indent=2)


class StranglingException(RuntimeError):

    def __init__(self, msg):
        super().__init__(msg)
