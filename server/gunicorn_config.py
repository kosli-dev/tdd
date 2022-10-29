from coverage import Coverage


def post_worker_init(worker):
    #print(dir(worker))
    print(f"post_worker_init {worker.pid=}", flush=True)
    cov = Coverage.current()
    cov.start()


def worker_exit(server, worker):
    #print(dir(server))
    print(f"worker_exit() {server.pid=} {worker.pid=}", flush=True)
    cov = Coverage.current()
    cov.stop()
    cov.save()  # pragma: no cover
