"""Automatic escalation for complaints past their resolution deadline."""

from datetime import datetime


DEFAULT_DEADLINE_DAYS = 3


def escalate_overdue_complaints(complaints, current_time=None):
    """Mark overdue unresolved complaints as escalated, exactly once."""
    now = current_time or datetime.now().astimezone()
    escalated_ids = []

    for complaint in complaints:
        if complaint.get("escalated") or complaint.get("status") == "Resolved":
            continue

        deadline = datetime.fromisoformat(complaint["deadline"])
        comparison_time = now
        if deadline.tzinfo is None and now.tzinfo is not None:
            deadline = deadline.replace(tzinfo=now.tzinfo)
        elif deadline.tzinfo is not None and now.tzinfo is None:
            comparison_time = now.replace(tzinfo=deadline.tzinfo)

        if comparison_time >= deadline:
            complaint["status"] = "Escalated"
            complaint["escalated"] = True
            complaint["escalation_date"] = now.isoformat(timespec="seconds")
            escalated_ids.append(complaint["complaint_id"])

    return escalated_ids
