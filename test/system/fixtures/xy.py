import json
import os
import pytest
import requests


@pytest.fixture
def xy():
    yield XY()


class XY:

    def score(self):
        url = score_url()
        payload = {}
        return http_get(url, payload)


def score_url():
    return f"/api/v1/score/"


def http_get(url, payload):
    headers = {'content-type': 'application/json'}
    data = json.dumps(payload, ensure_ascii=False).encode('utf8')
    return requests.get(f'{host()}{url}', headers=headers, data=data)


def host():
    return f'http://{service_name}:{port()}'


def port():
    return int(os.environ.get("XY_PORT"))


def service_name():
    # See docker-compose.yaml
    return 'xy'
