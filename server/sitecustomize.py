#!/usr/bin/env python3

import coverage

cov = coverage.process_startup()


def coverage_process_startup():
    global cov
    cov = coverage.process_startup()


def coverage_write_data():
    global cov
    cov.stop()
    cov.save()
    #cov.start()
    #del coverage.process_startup.coverage
    #cov = coverage.process_startup()


if __name__ == '__main__':
    coverage_process_startup()