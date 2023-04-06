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
        old_call = wrapped_call(old, old_is_main(use))
    if call_new(use):
        new_call = wrapped_call(new, new_is_main(use))

    if call_old(use) and call_new(use):
        strangled_check(cls, name, old_call, new_call)

    call = old_call if old_is_main(use) else new_call
    if exc := call["exception"]:
        raise exc
    else:
        return call["result"]


def wrapped_call(func, is_main):
    try:
        exception = None
        trace = ""
        result = func()
    except Exception as exc:
        exception = exc
        trace = traceback.format_exc()
        result = Raised()

    def safe_repr():
        try:
            return repr(func)
        except Exception as exc:
            return f"Exception: {exc}"

    return {
        "is": "primary" if is_main else "secondary",
        "result": result,
        "exception": exception,
        "trace": trace.split("\n"),
        "repr": safe_repr(),
        "args": func.args,
        "kwargs": func.kwargs
    }


def strangled_check(cls, name, old, new):
    old_exc, new_exc = old["exception"], new["exception"]
    exceptions = [old_exc, new_exc]

    # neither_raised = o_exc is None and n_exc is None
    # both_raised = not(o_exc is None or n_exc is None)

    if not any(exceptions):
        try:
            if old["result"] == new["result"]:
                return
            else:
                summary = "old['result'] == new['result'] --> False"
        except Exception as exc:
            summary = [
                "old['result'] == new['result'] --> raised!",
                str(exc)
            ]
    elif all(exceptions):
        if isinstance(old_exc, type(new_exc)):  # exceptions are the same type
            # If the real and fake raise the same exception (eg there is a bug in
            # a library they both use), this will swallow it and everything will
            # look OK. If you are not getting the expected strangler behaviour
            # consider putting a print/breakpoint here.
            return
        else:
            summary = "\n".join([
                "Different exception types",
                f"type(old['exception']) is {type(old_exc).__name__}",
                f"type(new['exception']) is {type(new_exc).__name__}"
            ])
    else:
        def raised(ex):
            return "raised" if ex is not None else "did not raise"
        summary = f"old {raised(old_exc)}, new {raised(new_exc)}"

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


class Raised:
    def __repr__(self):
        return 'Raised()'


class StrangledDifference(RuntimeError):

    def __init__(self, diff):
        self.diff = diff

    def __str__(self):
        return json.dumps(self.diff, indent=2)
