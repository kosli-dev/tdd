import coverage
import os
import subprocess


def xy_container_root_dir():
    return os.environ.get("XY_CONTAINER_ROOT_DIR")


def coverage_rc_file_path():
    return f"{xy_container_root_dir()}/test/system/.coveragerc"


def coverage_on_server():
    return os.environ.get("COVERAGE_PROCESS_START", False)


if coverage_on_server():
    cov = coverage.Coverage(config_file=coverage_rc_file_path())


def post_fork(server, worker):
    if coverage_on_server():
        recreate_coverage_dir()
        cov.start()


def worker_exit(server, worker):
    if coverage_on_server():
        try:
            cov.stop()
            cov.save()
        except:
            pass


def recreate_coverage_dir():
    cov_dir = os.environ.get("XY_CONTAINER_COV_DIR")
    rmdir_cmd = ["rm", "-rf", cov_dir]
    mkdir_cmd = ["mkdir", "-p", cov_dir]
    subprocess.run(rmdir_cmd, check=False)
    subprocess.run(mkdir_cmd, check=True)
