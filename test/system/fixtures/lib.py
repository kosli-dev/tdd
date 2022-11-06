import os
import requests
import textwrap


def http_get(url, **kwargs):
    return requests.get(f"{host()}{url}", json=kwargs)


def http_post(url, **kwargs):
    return requests.post(f"{host()}{url}",
                         json=kwargs)
                         # hooks={'response': print_round_trip})


def host():
    return f"http://{service_name()}:{port()}"


def port():
    # See scripts/echo_env_vars.sh
    return int(os.environ.get("XY_PORT"))


def service_name():
    # See docker-compose.yaml
    return 'xy'


def print_round_trip(response, *args, **kwargs):

    def format_headers(d):
        return '\n'.join(f'{k}: {v}' for k, v in d.items())

    print(textwrap.dedent('''
        ---------------- request ----------------
        {req.method} {req.url}
        {reqhdrs}

        {req.body}
        ---------------- response ----------------
        {res.status_code} {res.reason} {res.url}
        {reshdrs}

        {res.text}
    ''').format(
        req=response.request,
        res=response,
        reqhdrs=format_headers(response.request.headers),
        reshdrs=format_headers(response.headers),
    ))
