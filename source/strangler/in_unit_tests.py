import os


def in_unit_tests():
    test_mode = os.environ.get('TEST_MODE')
    return test_mode == 'unit'
