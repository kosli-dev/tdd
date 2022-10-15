
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
