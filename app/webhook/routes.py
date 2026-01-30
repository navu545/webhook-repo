from flask import Blueprint, jsonify, request, render_template
from datetime import datetime, timezone
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/receiver', methods=["POST"])


def receiver():

    if not payload:
        return jsonify({"msg": "invalid payload"}), 400
    
    payload = request.json
    event_type = request.headers.get("X-GitHub-Event")

    events = mongo.db.events

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if event_type == "push":
        data = {
            "request_id": payload["after"],
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": timestamp
        }

    elif event_type == "pull_request":
        pr = payload["pull_request"]

        if pr.get("merged"):
             
            data = {
                "request_id": str(pr["id"]),
                "author": pr["merged_by"]["login"],
                "action": "MERGE",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": timestamp
            }   

        else:
            data = {
                "request_id": str(pr["id"]),
                "author": pr["user"]["login"],
                "action": "PULL_REQUEST",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": timestamp
            }   

    else:
        return jsonify({"msg": "ignored"}), 200

    events.insert_one(data)
    return jsonify({"msg":"stored"}), 200


@webhook.route("/events", methods=["GET"])
def get_events():
    events = mongo.db.events.find().sort("timestamp", -1).limit(10)

    result = []
    for e in events:
        e["_id"] = str(e["_id"])
        result.append(e)

    return jsonify(result)    

@webhook.route("/", methods=["GET"])
def home():
    return render_template("index.html")


