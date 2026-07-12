from Lena.database import Database


class TaskRepository:

    def __init__(self):
        self.db = Database()

    def save(self, task):
        return self.db.save_task(task["id"], task)

    def get(self, task_id):
        return self.db.get_task(task_id)

    def delete(self, task_id):
        return self.db.delete_task(task_id)

    def get_all(self):
        return self.db.all_tasks()