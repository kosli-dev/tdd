import coverage
import os
import subprocess


def dot_coverage_dir():
    return f"{xy_app_dir()}/coverage/system"


def ls_coverage_dir():
    cmd = ["ls", "-al", "."]
    result = subprocess.run(cmd, cwd=dot_coverage_dir(), capture_output=True, text=True, check=True)
    print(result.stdout)


def config_file_path():
    return f"{xy_app_dir()}/test/system/.coveragerc"


def xy_app_dir():
    return os.environ.get("XY_APP_DIR")


cov = coverage.Coverage(config_file=config_file_path())


def post_fork(server, worker):
    # Start coverage right after the worker forks
    # print("Before post_fork()")
    # ls_coverage_dir()
    cov.start()
    # print("After post_fork()")
    # ls_coverage_dir()


def worker_exit(server, worker):
    # Save coverage when the worker finishes
    # print("Before worker_exit()")
    # ls_coverage_dir()
    # eg
    # -rw-r--r--    1 xy       xy           53248 Nov  1 13:00 .coverage.5c4ed550a9c7.11.975221
    # -rw-r--r--    1 xy       xy           53248 Nov  1 13:00 .coverage.5c4ed550a9c7.14.412705
    cov.stop()
    cov.save()
    # print("After worker_exit()")
    # ls_coverage_dir()
    # eg
    # -rw-r--r--    1 xy       xy           53248 Nov  1 13:00 .coverage.5c4ed550a9c7.11.975221
    # -rw-r--r--    1 xy       xy           53248 Nov  1 13:00 .coverage.5c4ed550a9c7.14.412705
    # -rw-r--r--    1 xy       xy           69632 Nov  1 13:01 .coverage.5c4ed550a9c7.24.950769
    # -rw-r--r--    1 xy       xy           69632 Nov  1 13:01 .coverage.5c4ed550a9c7.25.240037
