import coverage
import os
import subprocess


def xy_app_dir():
    return os.environ.get("XY_APP_DIR")


def config_file_path():
    return f"{xy_app_dir()}/test/system/.coveragerc"


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
    try:
        cov.stop()
        cov.save()
    except:
        pass
    # print("After worker_exit()")
    # ls_coverage_dir()


def dot_coverage_dir():
    return f"{xy_app_dir()}/coverage/system"


def ls_coverage_dir():
    cmd = ["ls", "-al", "."]
    result = subprocess.run(cmd,
                            cwd=dot_coverage_dir(),
                            capture_output=True,
                            text=True,
                            check=True)
    print(result.stdout)
