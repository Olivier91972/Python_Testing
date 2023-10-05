from datetime import datetime
import re


def date_is_passed(date) -> bool:
    """Return True if the variable date is passed or not"""
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    present = datetime.now()
    if date.date() < present.date():
        return True


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

