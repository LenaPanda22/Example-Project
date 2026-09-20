class StatisticsService:

    def __init__(self, task_repository):
        self.task_repository = task_repository

    def user_statistics(self, user_id):
        stats = {
            "total": 0,
            "new": 0,
            "in_progress": 0,
            "done": 0,
            "cancelled": 0,
            "overdue": 0,
        }

        for task in self.task_repository.get_all().values():

            if task.get("assignee") != user_id:
                continue

            stats["total"] += 1

            status = task.get("status")

            if status in (
                "new",
                "in_progress",
                "done",
                "cancelled",
            ):
                stats[status] += 1

        return stats