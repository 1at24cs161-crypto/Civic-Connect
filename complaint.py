"""Complaint record creation and display helpers."""

from datetime import datetime, timedelta
from uuid import uuid4

from routing import get_department


def create_complaint(
    citizen_name,
    phone_number,
    category,
    description,
    location,
    deadline_days=3,
):
    """Create a new complaint record with a unique ID and deadline."""
    registered_at = datetime.now().astimezone()
    return {
        "complaint_id": f"CC-{uuid4().hex[:8].upper()}",
        "citizen_name": citizen_name,
        "phone_number": phone_number,
        "category": category,
        "description": description,
        "location": location,
        "assigned_department": get_department(category),
        "status": "Pending",
        "registration_date": registered_at.isoformat(timespec="seconds"),
        "deadline": (registered_at + timedelta(days=deadline_days)).isoformat(
            timespec="seconds"
        ),
        "escalated": False,
        "escalation_date": None,
    }


def display_complaint(complaint):
    """Print all stored details for one complaint."""
    print("-" * 60)
    print(f"Complaint ID       : {complaint['complaint_id']}")
    print(f"Citizen name       : {complaint['citizen_name']}")
    print(f"Phone number       : {complaint['phone_number']}")
    print(f"Category           : {complaint['category']}")
    print(f"Description        : {complaint['description']}")
    print(f"Location           : {complaint['location']}")
    print(f"Department         : {complaint['assigned_department']}")
    print(f"Status             : {complaint['status']}")
    print(f"Registration date  : {complaint['registration_date']}")
    print(f"Resolution deadline: {complaint['deadline']}")
    print(f"Escalated          : {'Yes' if complaint['escalated'] else 'No'}")
    print(f"Escalation date    : {complaint['escalation_date'] or 'N/A'}")
    print("-" * 60)
