from flask import Blueprint, json, request, abort
from app.extensions import mongo, parse_time, get_gh_name
import hmac
import hashlib
import os

from dotenv import load_dotenv
load_dotenv()

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

GITHUB_SECRET = os.getenv("GH_SECRET")

@webhook.route("/receiver", methods=["POST"])
def receiver():
    # Verify signature
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        abort(400, "Missing signature")

    body = request.data
    expected = "sha256=" + hmac.new(
        GITHUB_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        abort(401, "Invalid signature")

    event = request.headers.get("X-GitHub-Event")
    print("Event:", event)

    if event == "ping":
        return {"msg": "pong"}, 200

    payload = request.json

    info = None
    if event == "push":
        info = get_push_info(payload)
    elif event == "pull_request" and payload["action"] == "opened":
        info = get_pr_info(payload)
    
    if info is not None:
        res = mongo.db.github.insert_one(info)
        print(res)

    return {"status": "ok"}, 200

def get_pr_info(payload) -> dict:
    info = {}
    info["request_id"] = payload["pull_request"]["number"]
    info["request_id"] = str(info["request_id"])
    info["author"] = payload["pull_request"]["user"]["login"]
    info["author"] = get_gh_name(info["author"])
    info["action"] = "PULL_REQUEST"
    info["from_branch"] = payload["pull_request"]["head"]["ref"].removeprefix("refs/heads/")
    info["to_branch"] = payload["pull_request"]["base"]["ref"].removeprefix("refs/heads/")
    info["timestamp"] = payload["pull_request"]["updated_at"]
    info["timestamp"] = parse_time(info["timestamp"])
    return info

def get_push_info(payload) -> dict:
    info = {}
    info["request_id"] = payload["head_commit"]["id"]
    info["author"] = payload["head_commit"]["author"]["name"]
    info["action"] = "PUSH"
    info["from_branch"] = "idk" # TODO: use github compare api which is smth like this: https://github.com/anamikapanickar09/action-repo/compare/10f6e7a4f6c8...0589748a1dd8
    info["to_branch"] = payload["ref"].removeprefix("refs/heads/")
    info["timestamp"] = payload["head_commit"]["timestamp"]
    info["timestamp"] = parse_time(info["timestamp"])
    return info
