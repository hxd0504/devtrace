from datetime import datetime, timezone


def append_activity_log(existing_log: list, user_id: int, username: str, action: str, details: str = None, **kwargs) -> list:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "user_id": user_id,
        "username": username,
        "action": action,
        "details": details,
        **kwargs,
    }
    return existing_log + [entry]
