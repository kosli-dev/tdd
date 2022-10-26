import json


def write_result(sid, result):
    with open(filename(sid), "w") as file:
        file.write(json.dumps(result))


def read_result(sid):
    with open(filename(sid), "r") as file:
        return json.loads(file.read())


def filename(sid):
    return f"/tmp/xy.{sid}.json"
