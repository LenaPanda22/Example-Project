# SCHICHT: Presentation / Entry-Point

from task_manager import TaskManager
from user import UserManager
from legacy.report_generator import ReportGenerator
from taskmaster.infrastructure.logger import log


def main():
    log("TaskMaster startet")

    um = UserManager()
    tm = TaskManager()
    rg = ReportGenerator()

    # Nutzer anlegen
    um.create_user(1, "Anna", "anna@example.com", "01701234567", "device-1")
    um.create_user(2, "Ben", "ben@example.com", "01709876543", "device-2")
    um.make_admin(1)

    # Aufgaben anlegen
    tm.create_task(101, "Landing Page bauen", "Neue Landing Page fuer Marketing", 2, 1, "2026-06-20", mode=1)
    tm.create_task(102, "Bug im Login", "Kritisch, viele Meldungen", 3, 2, "2026-05-15", mode=4)
    tm.create_task(103, "Doku schreiben", "Readme aktualisieren", 1, 2, "2026-06-30", mode=1)

    # Status aendern
    tm.update_status(101, "in_progress")
    tm.update_status(103, "done")

    print()
    print(rg.daily_report())
    print(rg.weekly_report())

    print()
    log("Mahnungen werden versendet...")
    tm.send_reminders()

    print()
    log("Aktuelle Aufgaben:")
    for k in tm.all_tasks():
        print("  " + tm.format_task(k))


if __name__ == "__main__":
    main()
