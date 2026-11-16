"""Input validation helpers used by the console application."""

import re

from routing import DEPARTMENT_BY_CATEGORY


CATEGORIES = tuple(DEPARTMENT_BY_CATEGORY)
STATUSES = ("Pending", "In Progress", "Resolved")


def require_text(prompt):
    """Prompt until the user enters non-empty text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def get_mobile_number(prompt="Enter 10-digit mobile number: "):
    """Prompt until a 10-digit mobile number is entered."""
    while True:
        phone_number = input(prompt).strip()
        if re.fullmatch(r"[0-9]{10}", phone_number):
            return phone_number
        print("Invalid mobile number. Enter exactly 10 digits.")


def choose_category():
    """Display categories and return a validated category selection."""
    print("\nComplaint categories:")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")

    while True:
        choice = input("Select category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("Invalid category selection. Choose one of the listed numbers.")


def choose_status():
    """Display available administrator status updates and return a selection."""
    print("\nAvailable statuses:")
    for number, status in enumerate(STATUSES, start=1):
        print(f"{number}. {status}")

    while True:
        choice = input("Select status number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(STATUSES):
            return STATUSES[int(choice) - 1]
        print("Invalid status selection. Choose one of the listed numbers.")
