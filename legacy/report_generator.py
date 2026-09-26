# SCHICHT: Application — Berichtserstellung

from datetime import datetime, timedelta
from taskmaster.infrastructure.database import Database
from user import UserManager
from taskmaster.infrastructure.logger import log


class ReportGenerator:
    def __init__(self):
        self.db = Database()
        self.users = UserManager()

    def daily_report(self):
        o = ""
        o = o + "=== TAGESBERICHT ===\n"
        o = o + "Datum: " + str(datetime.now().date()) + "\n"
        o = o + "\n"

        ts = self.db.all_tasks()
        c = datetime.now() - timedelta(days=1)

        n = 0
        d = 0
        op = 0

        for k in ts:
            t = ts[k]
            try:
                cr = datetime.fromisoformat(t.get("created", ""))
            except:
                continue
            if cr < c:
                continue
            if t["status"] == "new":
                n = n + 1
            elif t["status"] == "done":
                d = d + 1
            else:
                op = op + 1

        o = o + "Neu: " + str(n) + "\n"
        o = o + "Erledigt: " + str(d) + "\n"
        o = o + "Offen: " + str(op) + "\n"
        return o

    def weekly_report(self):
        o = ""
        o = o + "=== WOCHENBERICHT ===\n"
        o = o + "Woche ab: " + str(datetime.now().date()) + "\n"
        o = o + "\n"

        ts = self.db.all_tasks()
        c = datetime.now() - timedelta(days=7)

        n = 0
        d = 0
        op = 0

        for k in ts:
            t = ts[k]
            try:
                cr = datetime.fromisoformat(t.get("created", ""))
            except:
                continue
            if cr < c:
                continue
            if t["status"] == "new":
                n = n + 1
            elif t["status"] == "done":
                d = d + 1
            else:
                op = op + 1

        o = o + "Neu: " + str(n) + "\n"
        o = o + "Erledigt: " + str(d) + "\n"
        o = o + "Offen: " + str(op) + "\n"
        return o

    def monthly_report(self):
        o = ""
        o = o + "=== MONATSBERICHT ===\n"
        o = o + "Monat: " + str(datetime.now().date()) + "\n"
        o = o + "\n"

        ts = self.db.all_tasks()
        c = datetime.now() - timedelta(days=30)

        n = 0
        d = 0
        op = 0

        for k in ts:
            t = ts[k]
            try:
                cr = datetime.fromisoformat(t.get("created", ""))
            except:
                continue
            if cr < c:
                continue
            if t["status"] == "new":
                n = n + 1
            elif t["status"] == "done":
                d = d + 1
            else:
                op = op + 1

        o = o + "Neu: " + str(n) + "\n"
        o = o + "Erledigt: " + str(d) + "\n"
        o = o + "Offen: " + str(op) + "\n"
        return o

    def email_report(self, report_type, recipient):
        if report_type == "daily":
            content = self.daily_report()
        elif report_type == "weekly":
            content = self.weekly_report()
        elif report_type == "monthly":
            content = self.monthly_report()
        else:
            return False

        from taskmaster.infrastructure.email_service import EmailService
        es = EmailService()
        return es.send(recipient, "Bericht: " + report_type, content)
