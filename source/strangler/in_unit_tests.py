import os


def in_unit_tests():
    return os.environ.get('TEST_MODE') == 'unit'
