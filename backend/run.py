# app.py
import os
from datetime import datetime, timezone
from flask import Flask, request, jsonify, abort
from flask_cors import CORS 
from db import collection
from utils import verify_signature, format_time

app = Flask(__name__)
CORS(app)
# ---------- Webhook endpoint ----------
#for Icon
@app.route('/favicon.ico')
def favicon():
    return '', 204  # No Content


@app.route("/webhook", methods=["GET"])
def webhook_status():
    return jsonify({"status": "listening for GitHub POST events"}), 200

@app.route("/webhook", methods=["POST"])
def webhook():
    # 1. Verify signature
    if not verify_signature(request):
        abort(401, description="Invalid signature")

    event_type = request.headers.get("X-GitHub-Event", "unknown")
    payload = request.json or {}

    # 2. Dispatch handlers
    if event_type == "push":
        handle_push(payload)
    elif event_type == "pull_request":
        handle_pr(payload)
    # else ignore other events to keep code minimal

    return "", 204


def handle_push(payload):
    author = payload.get("pusher", {}).get("name", "unknown")
    to_branch = payload.get("ref", "").split("/")[-1] or "unknown"
    timestamp = format_time()

    doc = {
        "type": "push",
        "author": author,
        "to_branch": to_branch,
        "timestamp": timestamp,
        "raw": payload,                      # keep raw for debugging
        "created_at": datetime.utcnow(),
    }
    collection.insert_one(doc)


def handle_pr(payload):
    action = payload.get("action")
    pr = payload.get("pull_request", {})
    author = pr.get("user", {}).get("login", "unknown")
    from_branch = pr.get("head", {}).get("ref", "unknown")
    to_branch = pr.get("base", {}).get("ref", "unknown")
    timestamp = format_time()

    if action in ("opened", "reopened"):
        # PULL_REQUEST event
        doc = {
            "type": "pull_request",
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp,
            "raw": payload,
            "created_at": datetime.utcnow(),
        }
        collection.insert_one(doc)

    elif action == "closed" and pr.get("merged"):
        # MERGE (brownie points)
        doc = {
            "type": "merge",
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp,
            "raw": payload,
            "created_at": datetime.utcnow(),
        }
        collection.insert_one(doc)


# ---------- API for the UI ----------
@app.route("/events/latest", methods=["GET"])
def latest_events():
    """
    Return last N events sorted newest→oldest.
    UI can call: /events/latest?limit=10
    """
    limit = int(request.args.get("limit", 10))
    cursor = (
        collection.find({}, {"_id": 0, "raw": 0})  # hide _id & raw by default
        .sort("created_at", -1)
        .limit(limit)
    )
    return jsonify(list(cursor))


# ---------- Convenience ----------
@app.route("/", methods=["GET"])
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
