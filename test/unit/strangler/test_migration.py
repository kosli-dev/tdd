import pytest
from lib import ScopedMigration, ScopedCcMarkerFiles
from lib.contract_check import *
from lib.contract_check_decorators import contract_checked_method
from helpers.unit.lib.scoped_env_var import ScopedEnvVar
from .helpers import *


def test_ec291500():
    """
    During a migration, mongo code is not called, unless we are actually
    running the migration code
    """
    @contract_checked_method("f", use=APPEND_TEST, kind="query")
    class NotCalled:
        def __init__(self):
            self.overwrite = Func(lambda: 11)
            self.append = Func(lambda: raiser("raising an error"))
    d = NotCalled()

    with pytest.raises(ContractDifference):
        d.f()
        
    with ScopedMigration():
        with ScopedCcMarkerFiles(["NotCalled"]):
            d.f()

    with ScopedEnvVar('MONGO_MIGRATION', "True"):
        with ScopedMigration():
            with pytest.raises(ContractDifference):
                d.f()


class Func:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()

    def reset(self):
        pass
