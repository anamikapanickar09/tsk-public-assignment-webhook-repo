from flask_pymongo import PyMongo
from datetime import datetime, timezone
import requests

# Setup MongoDB here
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


# if __name__ == "__main__":

#     test_rows = [
#         {'request_id': '5be7406755fbfe86c77c5bf533d472fdc0b1122e', 'author': 'Anamika Panickar', 'action': 'PUSH', 'from_branch': 'idk', 'to_branch': 'main', 'timestamp': '2026-01-30T01:19:19+05:30'},
#         {'request_id': '915d55771fdfea253870b50c30ca3feadcf682db', 'author': 'Anamika Panickar', 'action': 'PUSH', 'from_branch': 'idk', 'to_branch': 'dev', 'timestamp': '2026-01-30T01:24:45+05:30'},
#         {'request_id': 'c00bd21943f0f255a8c38a25f4ea3ff8b7bd24a1', 'author': 'Anamika Panickar', 'action': 'PUSH', 'from_branch': 'idk', 'to_branch': 'dev', 'timestamp': '2026-01-30T01:22:16+05:30'},
#         {'request_id': 4, 'author': 'anamikapanickar09', 'action': 'PULL_REQUEST', 'from_branch': 'dev', 'to_branch': 'main', 'timestamp': '2026-01-29T19:55:24Z'},
#         {'request_id': 3, 'author': 'anamikapanickar09', 'action': 'PULL_REQUEST', 'from_branch': 'main', 'to_branch': 'dev', 'timestamp': '2026-01-29T19:51:28Z'},
#     ]
#     result = collection.insert_one(test_rows[0])
#     print(result)
