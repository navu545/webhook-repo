from flask import Blueprint, jsonify, request, render_template
from datetime import datetime, timezone
from app.extensions import mongo

# Blueprint for webhook related routes
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/receiver', methods=["POST"])


def receiver():

    """
    Receives GitHub webhook events (push, pull_request, merge),
    extracts minimal required fields and stores them in MongoDB.
    
    """

    #If payload didn't arrive, we wanna return early
    if not payload:
        return jsonify({"msg": "invalid payload"}), 400
    
    payload = request.json
    event_type = request.headers.get("X-GitHub-Event")

    # MongoDB collection
    events = mongo.db.events

    # Current UTC timestamp
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Handle PUSH event
    if event_type == "push":
        data = {
            "request_id": payload["after"],
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": timestamp
        }

    # Handle PULL REQUEST and MERGE events
    elif event_type == "pull_request":
        pr = payload["pull_request"]

        # If pull request was merged
        if pr.get("merged"):
             
            data = {
                "request_id": str(pr["id"]),
                "author": pr["merged_by"]["login"],
                "action": "MERGE",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": timestamp
            }   

        #Normal pull request
        else:
            data = {
                "request_id": str(pr["id"]),
                "author": pr["user"]["login"],
                "action": "PULL_REQUEST",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": timestamp
            }   

    # Ignore other GitHub events
    else:
        return jsonify({"msg": "ignored"}), 200

    # Store event in MongoDB
    events.insert_one(data)
    return jsonify({"msg":"stored"}), 200


@webhook.route("/events", methods=["GET"])
def get_events():

    """
    Returns latest 10 webhook events sorted by newest first.

    """
    events = mongo.db.events.find().sort("timestamp", -1).limit(10)

    result = []

    # Convert ObjectId to string for JSON serialization
    for e in events:
        e["_id"] = str(e["_id"])
        result.append(e)

    return jsonify(result)    

# Serve UI page
@webhook.route("/", methods=["GET"])
def home():

    """
    Returns the main UI page that displays
    latest GitHub activity.

    """
    return render_template("index.html")


