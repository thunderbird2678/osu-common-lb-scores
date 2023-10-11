import requests
import json
import math
import os.path

user1 = "reiji maigo"
user2 = "thunderbird2678"

url = "https://osustats.ppy.sh/api/getScores"

# get user 1 leaderboard scores
scores1 = []
body = {
    "page": "1",
    "u1": user1,
    "accMax": "100",
    "rankMax": "50",
    "gamemode": "0",
    "sortOrder": "0",
    "sortBy": "0",
    "resultType": "1"
}

response = requests.post(url, json=body)
pages = math.ceil(response.json()[1] / 24)

if (os.path.isfile(user1 + ".json")):

    # Opening JSON file
    f = open(user1 + ".json")
    scores1 = json.load(f)
else:
    for x in range(pages):
        print("page " + str(x+1) + " complete for " + user1)
        body["page"] = str(x+1)
        response = requests.post(url, json=body)
        data = response.json()
        for score in data[0]:
            scores1.append(score)

    with open(user1 + ".json", "w") as user1file:
        json.dump(scores1, user1file, indent=4)


# get user 2 leaderboard scores
scores2 = []
body = {
    "page": "1",
    "u1": user2,
    "accMax": "100",
    "rankMax": "50",
    "gamemode": "0",
    "sortOrder": "0",
    "sortBy": "0",
    "resultType": "1"
}

response = requests.post(url, json=body)
pages = math.ceil(response.json()[1] / 24)

if (os.path.isfile(user2 + ".json")):
    # Opening JSON file
    f = open(user2 + ".json")
    scores2 = json.load(f)
else:
    for x in range(pages):
        print("page " + str(x+1) + " complete for " + user2)
        body["page"] = str(x+1)
        response = requests.post(url, json=body)
        data = response.json()
        for score in data[0]:
            scores2.append(score)

    with open(user2 + ".json", "w") as user2file:
        json.dump(scores2, user2file, indent=4)

shortlist = scores2 if len(scores1) > len(scores2) else scores1
longlist = scores2 if len(scores1) < len(scores2) else scores1

common = []
for score in shortlist:
    match = next(
        (score2 for score2 in longlist if score2["beatmap"] == score["beatmap"]), False)
    if match:
        common.append({
            "map": score["beatmap"]["artist"] + " - " + score["beatmap"]["title"] + "[" + score["beatmap"]["version"] + "]",
            user1: {
                "position": score["position"],
                "rank": score["rank"],
                "score": score["score"],
                "maxCombo": score["maxCombo"],
                "accuracy": score["accuracy"],
                "enabledMods": score["enabledMods"],
                "playDate": score["playDate"],
                "ppValue": score["ppValue"],
            },
            user2: {
                "position": match["position"],
                "rank": match["rank"],
                "score": match["score"],
                "maxCombo": match["maxCombo"],
                "accuracy": match["accuracy"],
                "enabledMods": match["enabledMods"],
                "playDate": match["playDate"],
                "ppValue": match["ppValue"],
            }
        })

print(common)

with open("common.json", "w") as commonfile:
    json.dump(common, commonfile, indent=4)
