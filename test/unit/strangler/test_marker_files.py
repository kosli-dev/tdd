import pytest
from lib import ScopedCcMarkerFiles
from lib.contract_check import *
from lib.contract_check_decorators import contract_checked_method
from .helpers import *


def test_2500da00():
    """
    When use=APPEND_MAIN is True
    it drops back to NOT checking mongo when
    the marker file for the given class exists
    (which indicates the data for the class is currently being migrated)
    """
    @contract_checked_method("f", use=APPEND_MAIN, kind="query")
    class MarkedClass:
        def __init__(self):
            self.overwrite = FuncF(lambda: 17)
            self.append = FuncF(lambda: raiser("abc"))

    m = MarkedClass()

    with pytest.raises(RuntimeError) as exc:
        m.f()
    assert str(exc.value) == "abc"

    with ScopedCcMarkerFiles(["MarkedClass"]):
        m.f()


class FuncF:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()
