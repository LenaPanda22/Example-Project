class TaskRepository:

    def __init__(self, database):
        self.db = database

    def save(self, task):
        return self.db.save_task(task["id"], task)

    def get(self, task_id):
        return self.db.get_task(task_id)

    def delete(self, task_id):
        return self.db.delete_task(task_id)

    def get_all(self):
        return self.db.all_tasks()

    def find_tasks(self, status=None, priority=None, assignee_id=None):
        tasks = self.db.all_tasks()

        result = []

        for task in tasks.values():
            if status is not None and task.get("status") != status:
                continue

            if priority is not None and task.get("priority") != priority:
                continue

            if assignee_id is not None and task.get("assignee") != assignee_id:
                continue

            result.append(task)

        return result