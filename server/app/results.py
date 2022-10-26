import json
import secrets
from model import company_score


def write_result(data):
    score = company_score(decisions=data["decisions"],
                          is_sentence=data["is_sentence"],
                          is_profound=data["is_profound"])
    # TODO: create result from score
    result = {
        "squads": [
            {"char": "A", "letters": "xyzzy", "points": [4, 4, 15, 5, 6], "total": 34},
            {"char": "B", "letters": "hello", "points": [25, 25, 2, 2, 0], "total": 54},
            {"char": "C", "letters": "world", "points": [11, 11, 11, 11, 11], "total": 55},
        ],
        "total_score": 143
    }
    sid = secrets.token_urlsafe(6)
    with open(filename(sid), "w") as file:
        file.write(json.dumps(result))
    return sid


def read_result(sid):
    with open(filename(sid), "r") as file:
        return json.loads(file.read())


def filename(sid):
    return f"/tmp/xy.{sid}.json"
