from flask import Blueprint, jsonify
from app.extensions import mongo

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/get_events")
def get_events():
    events = list(
        mongo.db.github
        .find({}, {"_id": 0})
        .sort("_id", -1)
    )

    return jsonify(events)
