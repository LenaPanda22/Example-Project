from Refactorings.taskmaster.domain.user_types import AdminUser, ReadOnlyUser, User


class UserFactory:

    @staticmethod
    def build(data):

        if data is None:
            return None

        role = data.get("role")

        if role == "admin":
            return AdminUser(
                data["id"],
                data["name"],
                data["email"],
            )

        if role == "readonly":
            return ReadOnlyUser(
                data["id"],
                data["name"],
                data["email"],
            )

        return User(
            data["id"],
            data["name"],
            data["email"],
        )