from datetime import datetime


class ReminderService:
    def __init__(self, task_repository, notification_service):
        self.task_repository = task_repository
        self.notification_service = notification_service

    def find_overdue(self):
        overdue = []

        for task in self.task_repository.get_all().values():

            if task.get("due") is None:
                continue

            if task["status"] in ["done", "cancelled"]:
                continue

            try:
                due = datetime.fromisoformat(task["due"])
            #     TODO: too broad Exception
            except Exception:
                continue

            if due < datetime.now():
                overdue.append(task)

        return overdue

    def send_reminders(self):
        overdue = self.find_overdue()

        for task in overdue:
            self.notification_service.send_overdue_notification(task)