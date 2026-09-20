from Refactorings.taskmaster.domain.task import Priority

# Hinweis: Änderungen am NotificationService für Vorschläge 1&3 hängen zusammen
class NotificationService:

    def __init__(self, escalation_map, user_service):
        self._escalation = escalation_map
        self.user_service = user_service

    def send_new_task_notification(self, assignee_id, priority, title):
        user = self.user_service.get_user(assignee_id)

        if user is None:
            return False

        if priority == Priority.LOW:
            subject = "Neue Aufgabe (niedrig)"
        elif priority == Priority.MEDIUM:
            subject = "Neue Aufgabe (mittel)"
        elif priority == Priority.HIGH:
            subject = "Neue Aufgabe (hoch)"
        else:
            subject = "Neue Aufgabe"

        body = f"Dir wurde eine neue Aufgabe zugewiesen: {title}"

        notifier = self._escalation[priority]
        return notifier.notify(user, subject, body)

    def send_done_notification(self, task):
        user = self.user_service.get_user(task["assignee"])

        if user is None:
            return False

        return self._escalation[Priority.LOW].notify(
            user,
            "Aufgabe erledigt",
            f"Die Aufgabe '{task['title']}' ist erledigt."
        )

    def send_overdue_notification(self, task):
        user = self.user_service.get_user(task["assignee"])

        if user is None:
            return False

        notifier = self._escalation[task["priority"]]

        return notifier.notify(
            user,
            "Aufgabe überfällig",
            f"Die Aufgabe '{task['title']}' ist überfällig."
        )