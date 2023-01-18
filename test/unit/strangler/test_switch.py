from lib.contract_check import overwrite_is_on, append_is_on
from lib.contract_check import OVERWRITE_ONLY, APPEND_TEST, OVERWRITE_MAIN, APPEND_MAIN, APPEND_ONLY 


class Eg:
    def __init__(self, ow, ap):
        self.overwrite = ow
        self.append = ap


def test_eb760e00():
    """
    overwrite_is_on() is False only for APPEND_ONLY
    """
    eg = Eg(True, None)
    assert overwrite_is_on(eg, OVERWRITE_ONLY)
    assert overwrite_is_on(eg, APPEND_TEST)
    assert overwrite_is_on(eg, OVERWRITE_MAIN)
    assert overwrite_is_on(eg, APPEND_MAIN)
    assert overwrite_is_on(eg, APPEND_ONLY) is False


def test_eb760e01():
    """
    append_is_on() is False only for OVERWRITE_ONLY
    """
    eg = Eg(None, True)
    assert append_is_on(eg, OVERWRITE_ONLY) is False
    assert append_is_on(eg, APPEND_TEST)
    assert append_is_on(eg, OVERWRITE_MAIN)
    assert append_is_on(eg, APPEND_MAIN)
    assert append_is_on(eg, APPEND_ONLY)
