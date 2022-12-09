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
    squads = data["squads"]
    decisions = [[squad["letters"], squad["is_word"]] for squad in squads]
    all_scores = company_score(decisions=decisions,
                               is_sentence=data["is_sentence"],
                               is_profound=data["is_profound"])
    total_score = 0
    for i, scores in enumerate(all_scores):
        squads[i]["total"] = sum(scores)
        squads[i]["scores"] = scores
        total_score += sum(scores)

    return {
        "squads": squads,
        "total_score": f"{total_score:,}"  # eg "5,660"
    }
