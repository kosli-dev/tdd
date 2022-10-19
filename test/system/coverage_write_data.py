#!/usr/bin/env python3

from coverage import Coverage


if __name__ == "__main__":
    # TODO: Coverage's SIGTERM/SIGINT exit-handler
    #  writes pending coverage data to .coverage files
    #  ready for them to be combined and then reported.
    #  Hoping this would also write pending coverage data
    #  to .coverage files but alas it does not...
    Coverage().stop()
