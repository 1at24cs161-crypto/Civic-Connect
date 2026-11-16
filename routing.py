"""Category-to-department routing rules."""


DEPARTMENT_BY_CATEGORY = {
    "Water": "Water Supply Department",
    "Electricity": "Electricity Department",
    "Sanitation": "Sanitation Department",
    "Roads": "Road Maintenance Department",
}


def get_department(category):
    """Return the department responsible for a valid category."""
    try:
        return DEPARTMENT_BY_CATEGORY[category]
    except KeyError as error:
        raise ValueError(f"Unknown complaint category: {category}") from error
