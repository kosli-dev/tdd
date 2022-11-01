import coverage
import os


def config_file_path():
    xy_app_dir = os.environ.get("XY_APP_DIR")
    return f"{xy_app_dir}/test/system/.coveragerc"


cov = coverage.Coverage(config_file=config_file_path())


def post_fork(server, worker):
    # Start coverage right after the worker forks
    cov.start()


def worker_exit(server, worker):
    # Save coverage when the worker finishes
    cov.stop()
    cov.save()
