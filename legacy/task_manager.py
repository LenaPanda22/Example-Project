# SCHICHT: Application — Kern-Geschaeftslogik

from datetime import datetime, timedelta
from taskmaster.infrastructure.database import Database
from taskmaster.infrastructure.email_service import EmailService
from taskmaster.application.notifications import NotificationCenter
from user import UserManager
from taskmaster.infrastructure.logger import log, log_error, log_info, log_warning


class TaskManager:
    def __init__(self):
        self.db = Database()
        self.email = EmailService()
        self.notif = NotificationCenter()
        self.users = UserManager()
        self.cnt = 0

    def create_task(self, tid, title, desc, prio, assignee_id, due=None, mode=1):
        if title is None or title == "":
            log_error("Titel darf nicht leer sein")
            return False
        if prio < 1 or prio > 3:
            log_error("Prioritaet muss zwischen 1 und 3 liegen")
            return False

        t = {
            "id": tid,
            "title": title,
            "desc": desc,
            "priority": prio,
            "status": "new",
            "assignee": assignee_id,
            "created": str(datetime.now()),
            "due": due,
        }

        ok = self.db.save_task(tid, t)
        if not ok:
            return False

        u = self.users.get_user(assignee_id)
        if u is not None:
            if prio == 1:
                subject = "Neue Aufgabe (niedrig)"
            elif prio == 2:
                subject = "Neue Aufgabe (mittel)"
            elif prio == 3:
                subject = "Neue Aufgabe (hoch)"
            else:
                subject = "Neue Aufgabe"

            body = "Dir wurde eine neue Aufgabe zugewiesen: " + title

            if mode == 1:
                self.notif.notify(u, "email", subject, body)
            elif mode == 2:
                self.notif.notify(u, "sms", subject, body)
            elif mode == 3:
                self.notif.notify(u, "both", subject, body)
            elif mode == 4:
                self.notif.notify(u, "all", subject, body)

        self.cnt = self.cnt + 1
        log_info("Task " + str(tid) + " erstellt (Anzahl: " + str(self.cnt) + ")")
        return True

    def update_status(self, tid, new_status):
        t = self.db.get_task(tid)
        if t is None:
            log_error("Task nicht gefunden")
            return False

        if new_status not in ["new", "in_progress", "done", "cancelled"]:
            log_error("Unbekannter Status: " + str(new_status))
            return False

        old = t["status"]
        t["status"] = new_status
        self.db.save_task(tid, t)

        if new_status == "done":
            u = self.users.get_user(t["assignee"])
            if u is not None:
                self.notif.notify(
                    u, "email", "Aufgabe erledigt", "Die Aufgabe '" + t["title"] + "' ist erledigt."
                )

        log_info("Task " + str(tid) + ": " + old + " -> " + new_status)
        return True

    def delete_task(self, tid):
        t = self.db.get_task(tid)
        if t is None:
            return False
        self.db.delete_task(tid)
        log_warning("Task " + str(tid) + " geloescht")
        return True

    def get_task(self, tid):
        return self.db.get_task(tid)

    def all_tasks(self):
        return self.db.all_tasks()

    def format_task(self, tid):
        t = self.db.get_task(tid)
        if t is None:
            return "??"
        s = "#" + str(t["id"]) + " " + t["title"]
        if t["priority"] == 1:
            s = s + " [niedrig]"
        elif t["priority"] == 2:
            s = s + " [mittel]"
        elif t["priority"] == 3:
            s = s + " [hoch]"
        s = s + " (" + t["status"] + ")"
        return s

    def find_overdue(self):
        r = []
        for k in self.db.all_tasks():
            t = self.db.all_tasks()[k]
            if t.get("due") is None:
                continue
            if t["status"] == "done" or t["status"] == "cancelled":
                continue
            try:
                due = datetime.fromisoformat(t["due"])
            except:
                continue
            if due < datetime.now():
                r.append(t)
        return r

    def send_reminders(self):
        overdue = self.find_overdue()
        for t in overdue:
            u = self.users.get_user(t["assignee"])
            if u is None:
                continue
            if t["priority"] == 3:
                self.notif.notify_urgent(
                    u, "all", "Aufgabe ueberfaellig", "Die Aufgabe '" + t["title"] + "' ist ueberfaellig!"
                )
            elif t["priority"] == 2:
                self.notif.notify(
                    u, "both", "Aufgabe ueberfaellig", "Die Aufgabe '" + t["title"] + "' ist ueberfaellig."
                )
            else:
                self.notif.notify(
                    u, "email", "Aufgabe ueberfaellig", "Die Aufgabe '" + t["title"] + "' ist ueberfaellig."
                )
