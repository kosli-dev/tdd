import coverage
import os
import subprocess

# We send a SIGHUP to the master gunicorn process twice.
# Once before running the tests, one afterwards.
# The SIGHUP handling:
#   1. brings up the new workers and calls their post_fork()
#   2. brings down the old workers and calls their worker_exit()
# We rely on the ordering of 1) before 2).


cov = coverage.Coverage(config_file=os.environ["COVERAGE_PROCESS_START"])


def post_fork(server, worker):
    recreate_coverage_dir()
    cov.start()


def worker_exit(server, worker):
    cov.stop()
    cov.save()


def recreate_coverage_dir():
    cov_dir = os.environ["XY_CONTAINER_COV_DIR"]
    rmdir_cmd = ["rm", "-rf", cov_dir]
    mkdir_cmd = ["mkdir", "-p", cov_dir]
    subprocess.run(rmdir_cmd, check=False)
    subprocess.run(mkdir_cmd, check=True)
