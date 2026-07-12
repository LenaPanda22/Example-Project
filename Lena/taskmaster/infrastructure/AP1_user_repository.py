class UserRepository:

    def __init__(self, database):
        self.db = database

    def save(self, user):
        return self.db.save_user(user["id"], user)

    def get(self, uid):
        return self.db.get_user(uid)

    def get_all(self):
        return self.db.all_users()

    def delete(self, uid):
        return self.db.delete_user(uid)