class User:
    """Basisklasse fuer alle Benutzer."""

    def __init__(self, uid, name, email):
        self.uid = uid
        self.nm = name
        self.em = email

    def update_email(self, new_email):
        """Aktualisiert die E-Mail. Gibt True zurueck bei Erfolg."""
        self.em = new_email
        return True

    def delete_account(self):
        """Loescht den Account. Gibt True zurueck bei Erfolg."""
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
        raise PermissionError("Admin-Accounts koennen nicht geloescht werden")


class ReadOnlyUser(User):
    """Benutzer ohne Schreibrechte."""

    def update_email(self, new_email):
        raise PermissionError("ReadOnly-Benutzer koennen ihre E-Mail nicht aendern")

    def delete_account(self):
        raise PermissionError("ReadOnly-Benutzer koennen nicht geloescht werden")
