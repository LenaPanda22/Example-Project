# SCHICHT: Presentation / Entry-Point
from Refactorings.database import Database
from Refactorings.taskmaster.application.task_service import TaskService
from Refactorings.taskmaster.application.user_service import UserService
from Refactorings.taskmaster.application.reminder_service import ReminderService
from Refactorings.taskmaster.application.notification_service import NotificationService
from Refactorings.taskmaster.infrastructure.notifier_wiring import build_escalation
from Refactorings.taskmaster.infrastructure.notifiers import SmtpNotifier, PushNotifier, SmsNotifier
from Refactorings.taskmaster.infrastructure.task_repository import TaskRepository
from Refactorings.taskmaster.infrastructure.user_repository import UserRepository
from Refactorings.report_generator import ReportGenerator
from Refactorings.logger import log


def main():
    log("TaskMaster startet")

    # Repositories
    database = Database()
    task_repository = TaskRepository()
    user_repository = UserRepository(database)

    # Services
    user_service = UserService(user_repository)
    email_notifier = SmtpNotifier(
        "smtp.example.com",
        587,
        "user",
        "password"
    )

    sms_notifier = SmsNotifier()
    push_notifier = PushNotifier()

    escalation_map = build_escalation(
        email_notifier,
        sms_notifier,
        push_notifier
    )

    notification_service = NotificationService(
        escalation_map,
        user_service
    )
    reminder_service = ReminderService(task_repository, notification_service)

    user_service = UserService(user_repository)
    task_service = TaskService(task_repository,notification_service)

    # Report
    rg = ReportGenerator()

    # Nutzer anlegen
    user_service.create_user(
        1,
        "Anna",
        "anna@example.com",
        "01701234567",
        "device-1"
    )

    user_service.create_user(
        2,
        "Ben",
        "ben@example.com",
        "01709876543",
        "device-2"
    )

    user_service.make_admin(1)

    # Aufgaben anlegen
    task_service.create_task(
        101,
        "Landing Page bauen",
        "Neue Landing Page fuer Marketing",
        2,
        1,
        "2026-06-20",
        mode=1
    )

    task_service.create_task(
        102,
        "Bug im Login",
        "Kritisch, viele Meldungen",
        3,
        2,
        "2026-05-15",
        mode=4
    )

    task_service.create_task(
        103,
        "Doku schreiben",
        "Readme aktualisieren",
        1,
        2,
        "2026-06-30",
        mode=1
    )

    # Status aendern
    task_service.update_status(101, "in_progress")
    task_service.update_status(103, "done")

    print()
    print(rg.daily_report())
    print(rg.weekly_report())

    print()
    log("Mahnungen werden versendet...")
    reminder_service.send_reminders()

    print()
    log("Aktuelle Aufgaben:")
    for task in task_repository.get_all().values():
        print(task)


if __name__ == "__main__":
    main()