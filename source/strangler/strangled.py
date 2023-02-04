from copy import deepcopy
from datetime import datetime
import json
import threading
import time
import traceback
from .in_unit_tests import in_unit_tests
from .switch import *


def strangled(cls, name, use, old, new):
    """
    cls: eg User
    name: eg "login_id"
    use: eg OLD_MAIN
    """
    if call_old(use):
        old_call = wrapped_call(old, old_is_primary(use))
    if call_new(use):
        new_call = wrapped_call(new, new_is_primary(use))

    if call_both(use):
        strangled_check(cls, name, old_call, new_call)

    call = old_call if old_is_primary(use) else new_call
    if call["exception"] is None:
        return call["result"]
    else:
        raise call["exception"]


def wrapped_call(func, is_primary):
    try:
        exception = None
        trace = ""
        result = func()
    except Exception as exc:
        exception = exc
        trace = traceback.format_exc()
        result = NotSet()

    args = func.args
    kwargs = func.kwargs

    def safe_repr():
        try:
            return repr(func)
        except Exception as exc:
            return f"Exception: {exc}"

    return {
        "is": "primary" if is_primary else "secondary",
        "result": result,
        "exception": exception,
        "trace": trace.split("\n"),
        "repr": safe_repr(),
        "args": args,
        "kwargs": kwargs
    }


def strangled_check(cls, name, old, new):
    o_exc = old["exception"]
    n_exc = new["exception"]
    neither_raised = o_exc is None and n_exc is None
    both_raised = not(o_exc is None or n_exc is None)

    if neither_raised:
        try:
            if old["result"] == new["result"]:
                return
            else:
                summary = "old_result == new_result --> False"
        except Exception as exc:
            summary = "\n".join([
                "old_result == new_result --> raised",
                str(exc)
            ])
    elif both_raised:
        if type(o_exc) is type(n_exc):
            # If you have a typo in your program so that both raise AttributeError
            # for instance, the strangler will swallow that and everything looks OK.
            # So this is the place to put in a print if you don't understand why
            # your code does not give a strangler failure when you expect one.
            return
        else:
            summary = "\n".join([
                "type(old_exception) != type(new_exception)",
                f"type(old_exception) is {type(o_exc).__name__}",
                f"type(new_exception) is {type(n_exc).__name__}"
            ])
    else:
        def raised(ex):
            return "raised" if ex is not None else "did not raise"
        summary = f"old {raised(o_exc)}, new {raised(n_exc)}"

    def loggable(d):
        d = deepcopy(d)
        if d["exception"] is not None:
            d["exception"] = type(d["exception"]).__name__
        try:
            d["result"] = f"{repr(d['result'])}"
        except Exception as exc:
            d["result"] = [str(exc)] + traceback.format_exc().split("\n")
        return d

    diff = {
        "summary": summary,
        "time": now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "call": f"{cls.__name__}.{name}",
        "old": loggable(old),
        "new": loggable(new),
    }
    if in_unit_tests():
        raise StrangledDifference(diff)
    else:
        log_difference(diff)


def now():
    return datetime.utcfromtimestamp(time.time())


def log_difference(diff):
    with open(strangler_log_filename(), "a") as f:
        f.write(json.dumps(diff, indent=2))


def strangler_log_filename():
    tid = threading.get_ident()
    return f"/tmp/strangler_logs/log.{tid}"


class NotSet:
    def __repr__(self):
        return 'NotSet()'


class StrangledDifference(RuntimeError):

    def __init__(self, diff):
        self.diff = diff

    def __str__(self):
        return json.dumps(self.diff, indent=2)
