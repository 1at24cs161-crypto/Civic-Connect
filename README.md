# CivicConnect: Complaint Routing and Escalation System

## Introduction

CivicConnect is a beginner-friendly, terminal-based Python application for registering, routing, tracking, and escalating public-service complaints. It uses JSON files for permanent complaint storage and needs no third-party packages.

## Problem statement

Citizens may not know which public-service department should handle a concern, and unresolved requests can be difficult to track. CivicConnect gives each complaint a reference ID, routes it to the relevant department, and provides a simple way to track and administer its progress.

## Project objectives

- Register complaints with validated contact and issue details.
- Route Water, Electricity, Sanitation, and Roads complaints to the right department.
- Persist complaint records in JSON across application restarts.
- Allow citizens to track complaint and escalation details by ID.
- Give an administrator the ability to update status.
- Escalate unresolved overdue complaints once, recording the escalation time.

## Proposed solution

The console menu separates citizen features from administrator functions. Complaint records are dictionaries stored as a JSON list. Each new record receives a unique ID and a deadline three days after registration. An escalation check marks eligible unresolved records as `Escalated`. The deadline duration is configurable through `DEFAULT_DEADLINE_DAYS` in `escalation.py`.

## Technology stack

- Python 3 (standard library)
- JSON file storage
- `datetime` for registration, deadline, and escalation timestamps
- Git and GitHub for version control
- Visual Studio Code terminal

No web framework or external Python package is used.

## System architecture

1. `main.py` presents menus and coordinates application actions.
2. `validation.py` validates text, phone, category, and status input.
3. `routing.py` maps categories to departments.
4. `complaint.py` builds and displays complaint records.
5. `escalation.py` checks deadlines and updates eligible records.
6. `storage.py` reads and writes JSON, reporting corrupted or inaccessible data without replacing it.
7. `admin_config.py` keeps demonstration login values separate from citizen records.

## Folder structure

```text
CivicConnect/
├── main.py
├── complaint.py
├── routing.py
├── escalation.py
├── storage.py
├── validation.py
├── admin_config.py
├── data/
│   └── complaints.json
├── tests/
│   └── test_civicconnect.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Core features

- **Complaint registration:** asks for a name, 10-digit mobile number, category, description, and location; creates a unique ID, registration time, initial `Pending` status, and deadline.
- **Automatic routing:** Water → Water Supply Department; Electricity → Electricity Department; Sanitation → Sanitation Department; Roads → Road Maintenance Department.
- **Tracking and search:** displays complaint details, department, dates, status, and escalation state; unknown IDs receive a helpful message.
- **Administrator status management:** authenticated administrators can update statuses to Pending, In Progress, or Resolved. Credentials are `admin` / `admin123` for demonstration only. They are hardcoded, not secure; do not use these credentials or this login design in a real deployment.
- **Escalation:** after the configured deadline, unresolved complaints change to Escalated. The escalation flag and date prevent repeated escalation; resolved complaints are never escalated.
- **Additional views:** all complaints, department-wise complaints, pending/resolved/escalated lists, and summary counts.

## Data design

`data/complaints.json` contains a JSON array. Every item has:

`complaint_id`, `citizen_name`, `phone_number`, `category`, `description`, `location`, `assigned_department`, `status`, `registration_date`, `deadline`, `escalated`, and `escalation_date`.

Dates use ISO 8601 timestamps with local timezone information. The starter file contains an empty list. If the file is absent, CivicConnect treats the database as empty; if it is corrupted or unreadable, the application reports the problem and does not silently overwrite it.

## Install Python

1. Install a current Python 3 release from [python.org](https://www.python.org/downloads/).
2. On Windows, enable **Add Python to PATH** during installation if offered.
3. Open VS Code, open this project folder, and open **Terminal → New Terminal**.
4. Check the installation:

   ```powershell
   python --version
   ```

   If `python` is unavailable on Windows, try `py --version`.

## Run the project

In the VS Code terminal, from the project folder:

```powershell
python main.py
```

Alternatively:

```powershell
py main.py
```

No package installation is necessary. Complaint data is saved in `data/complaints.json`. Run the tests with:

```powershell
python -m unittest discover -s tests -v
```

## Sample terminal output

```text
============================================================
CIVICCONNECT: COMPLAINT ROUTING SYSTEM
============================================================
1. Register New Complaint
...
Select an option: 1

REGISTER NEW COMPLAINT
Citizen name: Asha Kumar
Enter 10-digit mobile number: 9876543210
Select category number: 1
Complaint description: Water leakage near the main road
Location: Ward 4

Complaint registered successfully.
Complaint ID: CC-6F1A2B3C
Assigned department: Water Supply Department
Resolution deadline: 2026-11-19T10:30:00+05:30
```

IDs and timestamps are generated at runtime. Tracking an existing ID displays the full record. An escalation check prints newly escalated IDs, or reports that no complaints are eligible.

## Testing and validation

Focused automated tests cover category routing, unique record IDs and deadlines, required fields and mobile/category input validation, escalation of overdue complaints, non-escalation of resolved and already escalated complaints, empty storage, and corrupted JSON handling. Run the command above to see test results.

## Limitations

- The administrator login uses demonstration-only hardcoded credentials and has no real identity management.
- JSON is appropriate for a small student demo, not concurrent multi-user or high-volume use.
- Escalations are checked when a user selects the escalation menu option; the program does not run as a background service.
- This is a console application and sends no notifications to citizens or departments.

## Future enhancements

- Use a database and secure, configurable administrator authentication.
- Add role-based access, audit history, and stronger input validation.
- Add configurable deadlines by category and reports/export.
- Send notifications and support department-side updates.

## GitHub upload instructions

From the project directory, create an empty repository on GitHub, then run:

```powershell
git init
git add .
git commit -m "Add CivicConnect complaint management project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your repository URL. Do not upload real personal information or production credentials.

## College evaluation explanation

CivicConnect applies modular programming: `main.py` coordinates the workflow, and each other module has a focused responsibility. A complaint enters as validated text, receives a generated ID and timestamp, is routed using a dictionary, and is written to JSON. Tracking loads the same record by ID. The administrator updates status after login. Escalation compares the current time with the stored deadline and writes the change once. The JSON file demonstrates persistence without requiring a database server.

## Suggested demonstration sequence

1. Start the program and register a sample Water complaint.
2. Note the ID and assigned Water Supply Department.
3. Track it by ID and demonstrate the registration date, status, and deadline.
4. Search a nonexistent ID to show the not-found handling.
5. Log in using the demonstration credentials and update the status to In Progress, then Resolved.
6. Use the test suite to demonstrate overdue escalation, resolved-item protection, and repeat-escalation protection without waiting three real days.
7. Show all complaints, department-wise views, statistics, and the persisted `data/complaints.json`.
"# CivicConnect" 
"# Civic-Connect" 
