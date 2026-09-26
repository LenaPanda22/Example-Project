class User:
    """Basisklasse für alle Benutzer."""

    def __init__(self, uid, name, email):
        self.uid = uid
        self.nm = name
        self.em = email

    def update_email(self, new_email):
        """Aktualisiert die E-Mail. Gibt True zurück bei Erfolg."""
        self.em = new_email
        return True

    def delete_account(self):
        """Löscht den Account. Gibt True zurück bei Erfolg."""
        return True

    def get_info(self):
        return self.nm + " (" + self.em + ")"


class AdminUser(User):
    def __init__(self, uid, name, email):
        super().__init__(uid, name, email)
        self.p = ["read", "write", "delete", "admin"]

    def update_email(self, new_email):
        self.em = new_email

    def delete_account(self):
        raise PermissionError("Admin-Accounts können nicht gelöscht werden")


class ReadOnlyUser(User):
    """Benutzer ohne Schreibrechte."""

    def update_email(self, new_email):
        raise PermissionError("ReadOnly-Benutzer können ihre E-Mail nicht ändern")

    def delete_account(self):
        raise PermissionError("ReadOnly-Benutzer können nicht gelöscht werden")
