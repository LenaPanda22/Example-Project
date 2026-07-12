from Lena.logger import log_error, log_info
from Lena.taskmaster.domain.user_types import AdminUser, ReadOnlyUser, User


class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, uid, name, email, phone="", device=""):

        if name is None or name == "":
            log_error("Name darf nicht leer sein")
            return False

        if email is None or "@" not in email:
            log_error("Ungueltige E-Mail")
            return False

        user = {
            "id": uid,
            "name": name,
            "email": email,
            "phone": phone,
            "device": device,
            "role": "user",
        }

        return self.user_repository.save(user)

    def make_admin(self, uid):

        user = self.user_repository.get(uid)

        if user is None:
            return False

        user["role"] = "admin"

        return self.user_repository.save(user)
    def is_admin(self, uid):

        user = self.user_repository.get(uid)

        return user is not None and user.get("role") == "admin"

    def get_user(self, uid):
        return self.user_repository.get(uid)

    def get_all(self):
        return self.user_repository.get_all()

    def build_user_obj(self, uid):

        data = self.user_repository.get(uid)

        if data is None:
            return None

        role = data.get("role")

        if role == "admin":
            return AdminUser(data["id"], data["name"], data["email"])

        if role == "readonly":
            return ReadOnlyUser(data["id"], data["name"], data["email"])

        return User(data["id"], data["name"], data["email"])

    def deactivate_user(self, uid):

        user = self.build_user_obj(uid)

        if user is None:
            return False

        return user.delete_account()

    def change_email(self, uid, new_email):

        user = self.build_user_obj(uid)

        if user is None:
            return False

        result = user.update_email(new_email)

        if result:
            log_info("E-Mail geaendert fuer " + str(uid))

        return result

    def format_user_for_report(self, uid):

        user = self.user_repository.get(uid)

        if user is None:
            return "Unbekannt"

        return user["name"] + " <" + user["email"] + ">"