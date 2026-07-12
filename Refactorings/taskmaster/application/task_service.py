from datetime import datetime
from Refactorings.logger import log_error, log_info, log_warning


class TaskService:
    def __init__(self, task_repository, notification_service):
        self.task_repository = task_repository
        self.notification_service = notification_service
        self.count = 0

    def create_task(self, tid, title, desc, prio, assignee_id, due=None, mode=1):

        if title is None or title == "":
            log_error("Titel darf nicht leer sein")
            return False

        if prio < 1 or prio > 3:
            log_error("Priorität muss zwischen 1 und 3 liegen")
            return False

        task = {
            "id": tid,
            "title": title,
            "desc": desc,
            "priority": prio,
            "status": "new",
            "assignee": assignee_id,
            "created": str(datetime.now()),
            "due": due,
        }

        if not self.task_repository.save(tid, task):
            return False

        self.notification_service.send_new_task_notification(
            assignee_id,
            prio,
            title,
            mode
        )

        self.count += 1
        log_info(f"Task {tid} erstellt (Anzahl: {self.count})")

        return True

    def update_status(self, tid, new_status):

        task = self.task_repository.get(tid)

        if task is None:
            log_error("Task nicht gefunden")
            return False

        if new_status not in ["new", "in_progress", "done", "cancelled"]:
            log_error("Unbekannter Status")
            return False

        old = task["status"]
        task["status"] = new_status

        self.task_repository.save(tid, task)

        if new_status == "done":
            self.notification_service.send_done_notification(task)

        log_info(f"Task {tid}: {old} -> {new_status}")

        return True

    def delete_task(self, tid):

        task = self.task_repository.get(tid)

        if task is None:
            return False

        self.task_repository.delete(tid)

        log_warning(f"Task {tid} gelöscht")

        return True

    def get_task(self, tid):
        return self.task_repository.get(tid)

    def all_tasks(self):
        return self.task_repository.get_all()

    def format_task(self, tid):

        task = self.task_repository.get(tid)

        if task is None:
            return "??"

        result = "#" + str(task["id"]) + " " + task["title"]

        if task["priority"] == 1:
            result += " [niedrig]"
        elif task["priority"] == 2:
            result += " [mittel]"
        elif task["priority"] == 3:
            result += " [hoch]"

        result += " (" + task["status"] + ")"

        return result