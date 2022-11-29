import os
import requests
import textwrap


def http_get(url, **kwargs):
    return requests.get(f"{host()}{url}", json=kwargs)


def http_post_files(url, **kwargs):
    return requests.post(f"{host()}{url}", data=kwargs)
                         # hooks={'response': print_round_trip})


def http_post_json(url, json):
    return requests.post(f"{host()}{url}", json=json)
                         # hooks={'response': print_round_trip})


def host():
    return f"http://{service_name()}:{port()}"


def port():
    return int(os.environ.get("XY_CONTAINER_PORT"))  # See scripts/lib.sh echo_env_vars()


def service_name():
    return 'xy_system'  # See docker-compose.yaml


def print_round_trip(response, *args, **kwargs):

    def format_headers(d):
        return '\n'.join(f'{k}: {v}' for k, v in d.items())

    print(textwrap.dedent('''
        ---------------- request ----------------
        {req.method} {req.url}
        {req_headers}

        {req.body}
        ---------------- response ----------------
        {res.status_code} {res.reason} {res.url}
        {res_headers}

        {res.text}
    ''').format(
        req=response.request,
        res=response,
        req_headers=format_headers(response.request.headers),
        res_headers=format_headers(response.headers),
    ))
