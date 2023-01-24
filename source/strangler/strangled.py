from copy import deepcopy
from datetime import datetime
import json
import threading
import time
import traceback
from .in_unit_tests import in_unit_tests
# from lib.diff import diff_only
from .log import set_strangler_log


def strangled(cls, name, use, old, new):
    """
    cls: eg User
    name: eg "login_id"
    use: eg OLD_MAIN
    """
    if use[0]:
        o = call(old)
        o["is"] = "primary" if old_is_primary(use) else "secondary"
    if use[1]:
        n = call(new)
        n["is"] = "primary" if new_is_primary(use) else "secondary"

    if use[0] and use[1]:
        strangled_check(cls.__name__, name, o, n)

    c = o if old_is_primary(use) else n
    if c["exception"] is None:
        return c["result"]
    else:
        raise c["exception"]


def call(func):
    try:
        exception = None
        trace = ""
        result = func()
    except Exception as exc:
        exception = exc
        trace = traceback.format_exc()
        result = "not-set"

    args = func.args
    kwargs = func.kwargs
    try:
        rep = repr(func)
    except Exception as exc:
        rep = str(exc)

    return {
        "result": result,
        "exception": exception,
        "trace": trace.split("\n"),
        "repr": rep,
        "args": args,
        "kwargs": kwargs
    }


def strangled_check(class_name, name, old, new):
    o_exc = old["exception"]
    n_exc = new["exception"]
    neither_raised = all(exc is None for exc in [o_exc, n_exc])
    both_raised = all(exc is not None for exc in [o_exc, n_exc])

    if neither_raised:
        try:
            if old["result"] == new["result"]:
                return
            else:
                summary = f"old_result == new_result --> False"
        except Exception as exc:
            summary = "\n".join([
                f"old_result == new_result --> raised",
                str(exc)
            ])
    elif both_raised:
        if type(o_exc) is type(n_exc):
            return
        else:
            summary = "\n".join([
                f"type(old_exc) != type(new_exc)",
                f"type(old_exc) is {type(o_exc).__name__}",
                f"type(new_exc) is {type(n_exc).__name__}"
            ])
    else:
        def raised(ex):
            return "raised" if ex is not None else "did not raise"
        summary = f"old {raised(o_exc)}, new {raised(n_exc)}"

    old = deepcopy(old)
    if old["exception"] is not None:
        old["exception"] = type(old["exception"]).__name__
    try:
        old["result"] = f"{repr(old['result'])}"
    except Exception as exc:
        old["result"] = [str(exc)] + traceback.format_exc().split("\n")

    new = deepcopy(new)
    if new["exception"] is not None:
        new["exception"] = type(new["exception"]).__name__
    try:
        new["result"] = f"{repr(new['result'])}"
    except Exception as exc:
        new["result"] = [str(exc)] + traceback.format_exc().split("\n")

    diff = {
        "summary": summary,
        "time": now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "class": class_name,
        "name": name,
        # "diff": diff_only(old_res, new_res)
        "old": old,
        "new": new,
    }

    if in_unit_tests():
        raise StrangledDifference(diff)
    else:
        log_difference(diff)


def now():
    return datetime.utcfromtimestamp(time.time())


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
        return json.dumps(self.diff, indent=2)
