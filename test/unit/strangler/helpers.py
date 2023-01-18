import json
from strangler import get_cc_log


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

