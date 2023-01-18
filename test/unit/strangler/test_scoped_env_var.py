import os
from .scoped_env_var import ScopedEnvVar


def test_e44512ed():
    """
    ScopedEnvVar sets env-var only inside with statement
    """
    name = "XXXXX"
    assert os.environ.get(name) is None
    with ScopedEnvVar(name, "42"):
        assert os.environ.get(name) == "42"
    assert os.environ.get(name) is None


def test_e44512ee():
    """
    ScopedEnvVar restores set env-var to its
    original value after the with statement
    """
    name = "YYYY"
    os.environ[name] = "HelloWorld"
    assert os.environ.get(name) == "HelloWorld"
    with ScopedEnvVar(name, "42"):
        assert os.environ.get(name) == "42"
    assert os.environ.get(name) == "HelloWorld"
