"""CivicConnect console application."""

from collections import Counter

from admin_config import ADMIN_PASSWORD, ADMIN_USERNAME
from complaint import create_complaint, display_complaint
from escalation import DEFAULT_DEADLINE_DAYS, escalate_overdue_complaints
from routing import DEPARTMENT_BY_CATEGORY
from storage import StorageError, load_complaints, save_complaints
from validation import choose_category, choose_status, get_mobile_number, require_text


SEPARATOR = "=" * 60


def find_complaint(complaints, complaint_id):
    """Find a complaint by its ID without regard to letter case."""
    normalized_id = complaint_id.strip().upper()
    return next(
        (
            complaint
            for complaint in complaints
            if complaint.get("complaint_id", "").upper() == normalized_id
        ),
        None,
    )


def print_complaints(complaints, heading="Complaints"):
    """Print a heading and complaint records, or a helpful empty message."""
    print(f"\n{heading}")
    print(SEPARATOR)
    if not complaints:
        print("No complaints found.")
        return
    for complaint in complaints:
        display_complaint(complaint)


def register_complaint():
    """Collect citizen details, route a complaint, and save it."""
    print("\nREGISTER NEW COMPLAINT")
    citizen_name = require_text("Citizen name: ")
    phone_number = get_mobile_number()
    category = choose_category()
    description = require_text("Complaint description: ")
    location = require_text("Location: ")

    complaints = load_complaints()
    complaint = create_complaint(
        citizen_name,
        phone_number,
        category,
        description,
        location,
        DEFAULT_DEADLINE_DAYS,
    )
    while find_complaint(complaints, complaint["complaint_id"]):
        complaint = create_complaint(
            citizen_name,
            phone_number,
            category,
            description,
            location,
            DEFAULT_DEADLINE_DAYS,
        )
    complaints.append(complaint)
    save_complaints(complaints)

    print("\nComplaint registered successfully.")
    print(f"Complaint ID: {complaint['complaint_id']}")
    print(f"Assigned department: {complaint['assigned_department']}")
    print(f"Resolution deadline: {complaint['deadline']}")


def track_complaint():
    """Find a complaint and display its complete details."""
    complaint_id = require_text("Enter complaint ID: ")
    complaint = find_complaint(load_complaints(), complaint_id)
    if complaint is None:
        print("Complaint ID not found. Please check the ID and try again.")
        return
    display_complaint(complaint)


def view_all_complaints():
    """Display every stored complaint."""
    print_complaints(load_complaints(), "ALL COMPLAINTS")


def search_complaint():
    """Search and display a complaint by ID."""
    complaint_id = require_text("Enter complaint ID to search: ")
    complaint = find_complaint(load_complaints(), complaint_id)
    if complaint is None:
        print("Complaint ID not found.")
        return
    display_complaint(complaint)


def view_department_complaints():
    """Display complaints assigned to a selected department."""
    categories = list(DEPARTMENT_BY_CATEGORY)
    print("\nDepartments:")
    for number, category in enumerate(categories, start=1):
        print(f"{number}. {DEPARTMENT_BY_CATEGORY[category]}")
    while True:
        choice = input("Select department number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            department = DEPARTMENT_BY_CATEGORY[categories[int(choice) - 1]]
            break
        print("Invalid department selection.")

    matches = [
        complaint
        for complaint in load_complaints()
        if complaint.get("assigned_department") == department
    ]
    print_complaints(matches, department.upper())


def check_escalations():
    """Escalate overdue complaints and persist any changes."""
    complaints = load_complaints()
    escalated_ids = escalate_overdue_complaints(complaints)
    if escalated_ids:
        save_complaints(complaints)
        print("Newly escalated complaint IDs:")
        for complaint_id in escalated_ids:
            print(f"- {complaint_id}")
    else:
        print("No complaints are overdue and eligible for escalation.")


def show_statistics():
    """Display totals by status, escalation, and department."""
    complaints = load_complaints()
    statuses = Counter(item.get("status", "Unknown") for item in complaints)
    escalated_count = sum(bool(item.get("escalated")) for item in complaints)

    print("\nCOMPLAINT STATISTICS")
    print(SEPARATOR)
    print(f"Total complaints: {len(complaints)}")
    print(f"Pending: {statuses.get('Pending', 0)}")
    print(f"In Progress: {statuses.get('In Progress', 0)}")
    print(f"Resolved: {statuses.get('Resolved', 0)}")
    print(f"Escalated: {escalated_count}")
    print("By department:")
    for department in DEPARTMENT_BY_CATEGORY.values():
        count = sum(
            item.get("assigned_department") == department for item in complaints
        )
        print(f"  {department}: {count}")


def update_complaint_status():
    """Update an existing complaint's status for an authenticated administrator."""
    complaint_id = require_text("Enter complaint ID to update: ")
    complaints = load_complaints()
    complaint = find_complaint(complaints, complaint_id)
    if complaint is None:
        print("Complaint ID not found.")
        return

    new_status = choose_status()
    complaint["status"] = new_status
    save_complaints(complaints)
    print(f"Status for {complaint['complaint_id']} updated to {new_status}.")


def administrator_menu():
    """Display administrator functions until logout."""
    while True:
        print(f"\n{SEPARATOR}\nADMINISTRATOR MENU\n{SEPARATOR}")
        print("1. View All Complaints")
        print("2. Update Complaint Status")
        print("3. View Pending Complaints")
        print("4. View Resolved Complaints")
        print("5. View Escalated Complaints")
        print("6. Check Escalations")
        print("7. Logout")
        choice = input("Select an option: ").strip()

        if choice == "1":
            view_all_complaints()
        elif choice == "2":
            update_complaint_status()
        elif choice == "3":
            complaints = load_complaints()
            print_complaints(
                [item for item in complaints if item.get("status") == "Pending"],
                "PENDING COMPLAINTS",
            )
        elif choice == "4":
            complaints = load_complaints()
            print_complaints(
                [item for item in complaints if item.get("status") == "Resolved"],
                "RESOLVED COMPLAINTS",
            )
        elif choice == "5":
            complaints = load_complaints()
            print_complaints(
                [item for item in complaints if item.get("escalated")],
                "ESCALATED COMPLAINTS",
            )
        elif choice == "6":
            check_escalations()
        elif choice == "7":
            print("Administrator logged out.")
            return
        else:
            print("Invalid menu selection. Choose a number from 1 to 7.")


def administrator_login():
    """Authenticate administrator before showing protected menu options."""
    print("\nADMINISTRATOR LOGIN")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
        print("Invalid administrator username or password.")
        return
    print("Login successful.")
    administrator_menu()


def main():
    """Run the main console menu."""
    while True:
        print(f"\n{SEPARATOR}\nCIVICCONNECT: COMPLAINT ROUTING SYSTEM\n{SEPARATOR}")
        print("1. Register New Complaint")
        print("2. Track Complaint")
        print("3. View All Complaints")
        print("4. Search Complaint")
        print("5. View Department-wise Complaints")
        print("6. Administrator Login")
        print("7. Check Automatic Escalations")
        print("8. View Complaint Statistics")
        print("9. Exit")
        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                register_complaint()
            elif choice == "2":
                track_complaint()
            elif choice == "3":
                view_all_complaints()
            elif choice == "4":
                search_complaint()
            elif choice == "5":
                view_department_complaints()
            elif choice == "6":
                administrator_login()
            elif choice == "7":
                check_escalations()
            elif choice == "8":
                show_statistics()
            elif choice == "9":
                print("Thank you for using CivicConnect. Goodbye!")
                return
            else:
                print("Invalid menu selection. Choose a number from 1 to 9.")
        except StorageError as error:
            print(f"\nData storage error: {error}")


if __name__ == "__main__":
    main()
