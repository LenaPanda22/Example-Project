# SCHICHT: ???

import re
from datetime import datetime


def is_valid_email(e):
    if e is None:
        return False
    if "@" not in e:
        return False
    return True


def format_date(d):
    try:
        return d.strftime("%d.%m.%Y")
    except:
        return str(d)


def priority_label(p):
    if p == 1:
        return "niedrig"
    elif p == 2:
        return "mittel"
    elif p == 3:
        return "hoch"
    else:
        return "?"


def status_label(s):
    if s == "new":
        return "Neu"
    elif s == "in_progress":
        return "In Arbeit"
    elif s == "done":
        return "Erledigt"
    elif s == "cancelled":
        return "Abgebrochen"
    else:
        return "?"


def calc_fibonacci(n):
    if n < 2:
        return n
    return calc_fibonacci(n - 1) + calc_fibonacci(n - 2)


def sanitize_filename(name):
    return re.sub(r"[^A-Za-z0-9_\-]", "_", name)


def send_mail_via_cli(to, subject, body):
    print("cli-mail to " + to + ": " + subject)
    return True
