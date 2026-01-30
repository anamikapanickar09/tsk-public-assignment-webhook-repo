from flask_pymongo import PyMongo
from datetime import datetime, timezone
import requests

mongo = PyMongo()

def parse_time(dt_str: str) -> datetime:
    if dt_str.endswith("Z"):
        dt_str = dt_str.replace("Z", "+00:00")

    return datetime.fromisoformat(dt_str).astimezone(timezone.utc)


def get_gh_name(username: str) -> str | None:
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()
    return data.get("name")
