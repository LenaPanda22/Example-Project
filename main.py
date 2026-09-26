# SCHICHT: Presentation / Entry-Point
from taskmaster.infrastructure.database import Database
from taskmaster.infrastructure.logger import log
from taskmaster.infrastructure.task_repository import TaskRepository
from taskmaster.infrastructure.user_repository import UserRepository
from taskmaster.infrastructure.notifiers import SmtpNotifier, PushNotifier, SmsNotifier
from taskmaster.infrastructure.notifier_wiring import build_escalation
from taskmaster.application.user_service import UserService
from taskmaster.application.notification_service import NotificationService
from taskmaster.application.task_service import TaskService
from taskmaster.application.reminder_service import ReminderService
from taskmaster.application.statistic_service import StatisticsService

def build_app():

    # Infrastruktur
    database = Database()
    task_repository = TaskRepository(database)
    user_repository = UserRepository(database)

    email = SmtpNotifier("smtp.example.com", 587, "user", "password")
    sms = SmsNotifier()
    push = PushNotifier()
    escalation = build_escalation(email, sms, push)

    # Application
    user_service = UserService(user_repository)
    notification_service = NotificationService(escalation, user_service)
    task_service = TaskService(task_repository, notification_service)
    reminder_service = ReminderService(task_repository, notification_service)
    statistics_service = StatisticsService(task_repository)

    return user_service, task_service, reminder_service, statistics_service


def main():
    log("TaskMaster startet")

    user_service, task_service, reminder_service, statistics_service = build_app()

    # Nutzer anlegen
    user_service.create_user(1, "Anna", "anna@example.com", "01701234567", "device-1")
    user_service.create_user(2, "Ben", "ben@example.com", "01709876543", "device-2")
    user_service.make_admin(1)

    # Aufgaben anlegen
    task_service.create_task(101, "Landing Page bauen", "Neue Landing Page fuer Marketing", 2, 1, "2026-06-20")
    task_service.create_task(102, "Bug im Login", "Kritisch, viele Meldungen", 3, 2, "2026-05-15")
    task_service.create_task(103, "Doku schreiben", "Readme aktualisieren", 1, 2, "2026-06-30")

    # Status ändern
    task_service.update_status(101, "in_progress")
    task_service.update_status(103, "done")

    # Erinnerungen für überfällige Aufgaben
    print()
    log("Mahnungen werden versendet...")
    reminder_service.send_reminders()

    # Neues Feature: Statistik pro Nutzer
    print()
    log("Statistik fuer Anna (Nutzer 1):")
    print("  " + str(statistics_service.user_statistics(1)))

    # Aktuelle Aufgaben
    print()
    log("Aktuelle Aufgaben:")
    for task_id in task_service.all_tasks():
        print("  " + task_service.format_task(task_id))


if __name__ == "__main__":
    main()
