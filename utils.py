import json
import os
import time
from datetime import datetime, timezone


def utc_now():
    return datetime.now(timezone.utc)


def utc_timestamp():
    return int(time.time())


def ensure_directory(path):
    os.makedirs(path, exist_ok=True)


def load_json(path, default=None):

    if default is None:
        default = {}

    if not os.path.exists(path):
        return default

    try:
        with open(path, "r") as f:
            return json.load(f)

    except Exception:
        return default


def save_json(path, data):

    folder = os.path.dirname(path)

    if folder:
        ensure_directory(folder)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def percentage_change(old, new):

    if old == 0:
        return 0

    return ((new - old) / old) * 100


def clamp(value, minimum, maximum):

    return max(minimum, min(value, maximum))


def log(message):

    print(
        f"[{utc_now().strftime('%Y-%m-%d %H:%M:%S UTC')}] {message}"
    )