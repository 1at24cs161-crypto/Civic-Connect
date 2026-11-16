"""Focused tests for CivicConnect's core data and validation behavior."""

import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from complaint import create_complaint
from escalation import escalate_overdue_complaints
from main import administrator_login, find_complaint
from routing import get_department
from storage import StorageError, load_complaints, save_complaints
from validation import choose_category, choose_status, get_mobile_number, require_text


class ComplaintTests(unittest.TestCase):
    def test_create_complaint_routes_and_sets_three_day_deadline(self):
        complaint = create_complaint(
            "Asha", "9876543210", "Water", "Leak", "Ward 4"
        )
        registered = datetime.fromisoformat(complaint["registration_date"])
        deadline = datetime.fromisoformat(complaint["deadline"])

        self.assertEqual(complaint["assigned_department"], "Water Supply Department")
        self.assertEqual(complaint["status"], "Pending")
        self.assertFalse(complaint["escalated"])
        self.assertEqual(deadline - registered, timedelta(days=3))

    def test_complaint_ids_are_unique(self):
        records = [
            create_complaint("A", "9876543210", "Roads", "Issue", "Here")
            for _ in range(20)
        ]
        self.assertEqual(len({record["complaint_id"] for record in records}), 20)

    def test_all_categories_have_department_mapping(self):
        self.assertEqual(
            get_department("Electricity"), "Electricity Department"
        )
        with self.assertRaises(ValueError):
            get_department("Unknown")


class ValidationTests(unittest.TestCase):
    def test_empty_name_and_invalid_phone_are_rejected(self):
        with patch("builtins.input", side_effect=["", "Asha"]):
            self.assertEqual(require_text("Name: "), "Asha")
        with patch("builtins.input", side_effect=["123", "1234567890"]):
            self.assertEqual(get_mobile_number(), "1234567890")

    def test_invalid_category_selection_is_rejected(self):
        with patch("builtins.input", side_effect=["bad", "9", "2"]):
            self.assertEqual(choose_category(), "Electricity")

    def test_invalid_status_selection_is_rejected(self):
        with patch("builtins.input", side_effect=["bad", "4", "2"]):
            self.assertEqual(choose_status(), "In Progress")

    def test_non_ascii_digits_are_not_accepted_as_mobile_number(self):
        with patch("builtins.input", side_effect=["１２３４５６７８９０", "1234567890"]):
            self.assertEqual(get_mobile_number(), "1234567890")


class ApplicationTests(unittest.TestCase):
    def test_complaint_id_search_is_case_insensitive_and_handles_unknown_ids(self):
        complaint = {"complaint_id": "CC-ABC123"}
        self.assertIs(find_complaint([complaint], "cc-abc123"), complaint)
        self.assertIsNone(find_complaint([complaint], "CC-MISSING"))

    def test_invalid_administrator_login_does_not_open_admin_menu(self):
        with patch("builtins.input", side_effect=["wrong", "wrong"]), patch(
            "main.administrator_menu"
        ) as menu:
            with redirect_stdout(StringIO()):
                administrator_login()
        menu.assert_not_called()


class EscalationTests(unittest.TestCase):
    def test_overdue_unresolved_record_escalates_once(self):
        now = datetime(2026, 1, 10, tzinfo=timezone.utc)
        overdue = {
            "complaint_id": "CC-OVERDUE",
            "status": "Pending",
            "deadline": (now - timedelta(seconds=1)).isoformat(),
            "escalated": False,
            "escalation_date": None,
        }
        resolved = dict(overdue, complaint_id="CC-RESOLVED", status="Resolved")
        already_escalated = dict(
            overdue, complaint_id="CC-DONE", escalated=True
        )
        complaints = [overdue, resolved, already_escalated]

        self.assertEqual(
            escalate_overdue_complaints(complaints, now), ["CC-OVERDUE"]
        )
        self.assertEqual(overdue["status"], "Escalated")
        self.assertEqual(
            overdue["escalation_date"], now.isoformat(timespec="seconds")
        )
        self.assertEqual(escalate_overdue_complaints(complaints, now), [])
        self.assertEqual(resolved["status"], "Resolved")

    def test_not_yet_overdue_record_is_not_escalated(self):
        now = datetime(2026, 1, 10, tzinfo=timezone.utc)
        complaint = {
            "complaint_id": "CC-FUTURE",
            "status": "In Progress",
            "deadline": (now + timedelta(seconds=1)).isoformat(),
            "escalated": False,
            "escalation_date": None,
        }
        self.assertEqual(escalate_overdue_complaints([complaint], now), [])


class StorageTests(unittest.TestCase):
    def test_missing_and_empty_database_load_as_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "complaints.json")
            self.assertEqual(load_complaints(path), [])
            save_complaints([], path)
            self.assertEqual(load_complaints(path), [])

    def test_corrupted_json_is_reported_without_replacement(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "complaints.json")
            with open(path, "w", encoding="utf-8") as data_file:
                data_file.write("{broken")
            with self.assertRaises(StorageError):
                load_complaints(path)
            with open(path, "r", encoding="utf-8") as data_file:
                self.assertEqual(data_file.read(), "{broken")

    def test_records_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "nested", "complaints.json")
            records = [create_complaint("Asha", "9876543210", "Roads", "Pothole", "Ward 2")]
            save_complaints(records, path)
            self.assertEqual(load_complaints(path), records)
            with open(path, "r", encoding="utf-8") as data_file:
                self.assertIsInstance(json.load(data_file), list)


if __name__ == "__main__":
    unittest.main()
