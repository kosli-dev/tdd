import os
from .helpers import ScopedEnvVar


def test_4512ed():
    """
    ScopedEnvVar sets env-var only inside with statement
    """
    name = "XXXXX"
    assert os.environ.get(name) is None
    with ScopedEnvVar(name, "42"):
        assert os.environ.get(name) == "42"
        assert os.environ[name] == "42"

    assert os.environ.get(name) is None


def test_4512ee():
    """
    ScopedEnvVar restores set env-var to its
    original value after the with statement
    """
    name = "YYYY"
    os.environ[name] = "HelloWorld"
    assert os.environ.get(name) == "HelloWorld"
    with ScopedEnvVar(name, "42"):
        assert os.environ.get(name) == "42"
        assert os.environ[name] == "42"
    assert os.environ.get(name) == "HelloWorld"
