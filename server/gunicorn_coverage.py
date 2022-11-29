import coverage
import os
import subprocess


def xy_container_dir():
    return os.environ.get("XY_CONTAINER_DIR")


def coverage_rc_file_path():
    return f"{xy_container_dir()}/test/system/.coveragerc"


def coverage_on_server():
    return os.environ.get("COVERAGE_PROCESS_START", None)


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
    # Note: dir is a tmpfs
    # This needs to work on localhost and CI run.
    dir = f"{xy_container_dir()}/coverage/system"
    rm = ["rm", "-rf", dir]
    subprocess.run(rm, cwd='/xy', capture_output=True, text=True, check=False)
    mkdir = ["mkdir", "-p", dir]
    subprocess.run(mkdir, cwd='/xy', capture_output=True, text=True, check=True)
