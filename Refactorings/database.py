# SCHICHT: Infrastruktur — Persistenz

import json
import os
from logger import log, log_error
from config import DB_FILE, USER_FILE


class Database:
    def __init__(self):
        self.d = {}
        self.u = {}
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        self.load()

    def load(self):
        if os.path.exists(DB_FILE):
            f = open(DB_FILE, "r")
            try:
                self.d = json.loads(f.read())
            except:
                log_error("Konnte tasks.json nicht laden")
                self.d = {}
            f.close()
        else:
            self.d = {}

        if os.path.exists(USER_FILE):
            f = open(USER_FILE, "r")
            try:
                self.u = json.loads(f.read())
            except:
                log_error("Konnte users.json nicht laden")
                self.u = {}
            f.close()
        else:
            self.u = {}

    def save(self):
        f = open(DB_FILE, "w")
        f.write(json.dumps(self.d))
        f.close()
        f = open(USER_FILE, "w")
        f.write(json.dumps(self.u))
        f.close()
        log("Gespeichert")

    # Tasks
    def get_task(self, tid):
        if str(tid) in self.d:
            return self.d[str(tid)]
        return None

    def save_task(self, tid, task):
        if task.get("title") is None or task.get("title") == "":
            log_error("Task ohne Titel kann nicht gespeichert werden")
            return False
        if task.get("priority", 0) < 1 or task.get("priority", 0) > 3:
            log_error("Ungueltige Prioritaet")
            return False
        self.d[str(tid)] = task
        self.save()
        return True

    def delete_task(self, tid):
        if str(tid) in self.d:
            del self.d[str(tid)]
            self.save()

    def all_tasks(self):
        return self.d

    # Users
    def get_user(self, uid):
        if str(uid) in self.u:
            return self.u[str(uid)]
        return None

    def save_user(self, uid, user):
        if user.get("name") is None or user.get("name") == "":
            log_error("User ohne Name kann nicht gespeichert werden")
            return False
        self.u[str(uid)] = user
        self.save()
        return True

    def delete_user(self, uid):
        if str(uid) in self.u:
            del self.u[str(uid)]
            self.save()

    def all_users(self):
        return self.u
