import json
import secrets
from model import company_score


def write_result(data):
    sid = secrets.token_urlsafe(6)
    with open(filename(sid), "w") as file:
        file.write(json.dumps(scored(data)))
    return sid


def read_result(sid):
    with open(filename(sid), "r") as file:
        return json.loads(file.read())


def filename(sid):
    return f"/tmp/xy.{sid}.json"


def scored(data):
    decisions = data["decisions"]
    scores = company_score(decisions=decisions,
                           is_sentence=data["is_sentence"],
                           is_profound=data["is_profound"])
    total_score = 0
    squads = []
    for i, score in enumerate(scores):
        squads.append({
            "char": chr(ord('a') + i).upper(),
            "letters": decisions[i][0],
            "points": score,
            "total": sum(score)
        })
        total_score += sum(score)

    return {"squads": squads, "total_score": total_score}
