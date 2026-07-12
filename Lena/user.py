# SCHICHT: Application — Benutzer-Verwaltung

from database import Database
from logger import log, log_error
from user_types import User, AdminUser, ReadOnlyUser


class UserManager:
    def __init__(self):
        self.db = Database()

    def create_user(self, uid, name, email, phone="", device=""):
        if name is None or name == "":
            log_error("Name darf nicht leer sein")
            return False
        if email is None or "@" not in email:
            log_error("Ungueltige E-Mail")
            return False

        u = {
            "id": uid,
            "name": name,
            "email": email,
            "phone": phone,
            "device": device,
            "role": "user",
        }
        return self.db.save_user(uid, u)

    def make_admin(self, uid):
        u = self.db.get_user(uid)
        if u is None:
            return False
        u["role"] = "admin"
        return self.db.save_user(uid, u)

    def is_admin(self, uid):
        u = self.db.get_user(uid)
        if u is None:
            return False
        if u.get("role") == "admin":
            return True
        return False

    def get_user(self, uid):
        return self.db.get_user(uid)

    def get_all(self):
        return self.db.all_users()

    def build_user_obj(self, uid):
        """Gibt ein User-Objekt passend zur Rolle zurueck."""
        d = self.db.get_user(uid)
        if d is None:
            return None
        if d.get("role") == "admin":
            return AdminUser(d["id"], d["name"], d["email"])
        if d.get("role") == "readonly":
            return ReadOnlyUser(d["id"], d["name"], d["email"])
        return User(d["id"], d["name"], d["email"])

    def deactivate_user(self, uid):
        """Deaktiviert einen Benutzer."""
        u = self.build_user_obj(uid)
        if u is None:
            return False
        return u.delete_account()

    def change_email(self, uid, new_email):
        """Aendert die E-Mail eines Benutzers."""
        u = self.build_user_obj(uid)
        if u is None:
            return False
        result = u.update_email(new_email)
        if result:
            log("E-Mail geaendert fuer " + str(uid))
        return result

    def format_user_for_report(self, uid):
        u = self.db.get_user(uid)
        if u is None:
            return "Unbekannt"
        return u["name"] + " <" + u["email"] + ">"
