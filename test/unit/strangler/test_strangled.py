import pytest
from strangler import *
from .helpers import *
import json


def XX_test_bba0d0():
    """
    """
    @strangled_method("f", use=NEW_TEST)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 17)
            self.new = None

    d = Different()
    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        d.f()

    assert no_strangler_logging()


class FuncF:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()
