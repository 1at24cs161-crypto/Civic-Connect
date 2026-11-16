"""JSON file persistence for complaint records."""

import json
import os


DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "complaints.json")


class StorageError(Exception):
    """Raised when complaint data cannot safely be read or written."""


def load_complaints(file_path=DATA_FILE):
    """Load complaints from JSON; report malformed files without replacing them."""
    try:
        with open(file_path, "r", encoding="utf-8") as data_file:
            complaints = json.load(data_file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise StorageError(
            f"The complaint data file is corrupted or unreadable: {error}"
        ) from error
    except OSError as error:
        raise StorageError(f"Could not read complaint data: {error}") from error

    if not isinstance(complaints, list) or not all(
        isinstance(item, dict) for item in complaints
    ):
        raise StorageError("Complaint data must be a JSON list of complaint records.")
    return complaints


def save_complaints(complaints, file_path=DATA_FILE):
    """Write all complaint records through a temporary file before replacing data."""
    directory = os.path.dirname(os.path.abspath(file_path))
    temporary_path = file_path + ".tmp"
    try:
        os.makedirs(directory, exist_ok=True)
        with open(temporary_path, "w", encoding="utf-8") as data_file:
            json.dump(complaints, data_file, indent=4, ensure_ascii=False)
            data_file.write("\n")
        os.replace(temporary_path, file_path)
    except (OSError, TypeError, ValueError) as error:
        raise StorageError(f"Could not save complaint data: {error}") from error
