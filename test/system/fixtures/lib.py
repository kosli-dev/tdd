import os, requests


def http_get(url, **kwargs):
    return requests.get(f"{host()}{url}", json=kwargs)


def http_post(url, **kwargs):
    return requests.post(f"{host()}{url}",  json=kwargs)


def host():
    return f"http://{service_name()}:{port()}"


def port():
    # See scripts/echo_env_vars.sh
    return int(os.environ.get("XY_PORT"))


def service_name():
    # See docker-compose.yaml
    return 'xy'
