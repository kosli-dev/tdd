from coverage import Coverage


def post_worker_init(worker):
    cov = Coverage.current()
    cov.start()


def worker_exit(server, worker):
    cov = Coverage.current()
    cov.stop()
    cov.save()  # pragma: no cover
