ISSUE_TRANSITIONS = {
    "open": ["in_progress"],
    "in_progress": ["resolved", "open"],
    "resolved": ["archived", "in_progress"],
    "archived": [],
}

TASK_TRANSITIONS = {
    "todo": ["doing"],
    "doing": ["done", "todo"],
    "done": ["doing"],
}


def can_transition_issue(current_status: str, target_status: str) -> bool:
    return target_status in ISSUE_TRANSITIONS.get(current_status, [])


def can_transition_task(current_status: str, target_status: str) -> bool:
    return target_status in TASK_TRANSITIONS.get(current_status, [])


def validate_archive_fields(data: dict) -> list[str]:
    errors = []
    if not data.get("root_cause"):
        errors.append("root_cause 为必填项")
    if not data.get("failed_attempts"):
        errors.append("failed_attempts 为必填项")
    if not data.get("final_solution"):
        errors.append("final_solution 为必填项")
    if data.get("reusable") is None:
        errors.append("reusable 为必填项")
    return errors
