
def pytest_configure(config):
    """
    run.sh test files contain two flags
      pytest --quiet --random-order-bucket=global ...
    which means the random-order seed used is not printed.
    Print it (in the format needed) before any tests run so
    we can re-run exactly the same failures when needed.
    """
    flag = "--random-order-seed"
    value = config.getoption(flag)
    if value.startswith('default:'):
        seed = value.split(':')[1]  # 'default:48756'
    else:
        seed = value  # '48756'
    print(f"{flag}={seed}")


def pytest_addoption(parser):
    """
    The tests are written like this:
      def test_fca44b75():
    The intention of the test is not conveyed in its name, but in
    its docstring. This means you cannot use pytest's -k flag to
    selectively run tests matching words in the test's name.
    Instead we add a --ds flag to selectively run tests matching
    words in the test's docstring.
    """
    parser.addoption(
        "--ds", action="append", help="Only run tests with matching docstrings"
    )


def pytest_collection_modifyitems(session, config, items):
    filter_strings = config.getoption('--ds')
    if filter_strings is None:
        return

    def doc_string_match(item):
        ds = item.function.__doc__
        if ds is None:
            print(f"No docstring for {item.function.__name__}")
            return False
        else:
            return any(fs for fs in filter_strings if fs in ds)

    keep = [item for item in items if doc_string_match(item)]
    items.clear()
    items.extend(keep)
    for k in keep:
        print(f"--ds {k.function.__name__}")
