import json, os, pytest, requests


@pytest.fixture
def xy():
    yield XY()


class XY:

    def health_ready(self):
        return http_get('/api/health/ready')

    def company_score(self, **kwargs):
        return http_post("/api/company/score", **kwargs)


def http_get(url, **kwargs):
    headers = {"content-type": "application/json"}
    data = json.dumps(kwargs, ensure_ascii=False).encode("utf8")
    return requests.get(f"{host()}{url}", headers=headers, data=data)


def http_post(url, **kwargs):
    headers = {"content-type": "application/json"}
    data = json.dumps(kwargs, ensure_ascii=False).encode("utf8")
    return requests.post(f"{host()}{url}", headers=headers, data=data)


def host():
    return f"http://{service_name()}:{port()}"


def port():
    # See scripts/echo_env_vars.sh
    return int(os.environ.get("XY_PORT"))


def service_name():
    # See docker-compose.yaml
    return 'xy'
