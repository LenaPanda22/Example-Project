import unittest
from datetime import datetime, timedelta

from Refactorings.taskmaster.domain.task import (
    Task,
    Priority,
    Status,
    DomainError,
)


class TestTask(unittest.TestCase):

    # Testet, ob beim Erstellen einer Aufgabe mit leerem Titel
    # korrekt ein DomainError ausgelöst wird.
    def test_task_mit_leerem_titel_wirft_fehler(self):
        with self.assertRaises(DomainError):
            Task(
                id=1,
                title="",
                priority=Priority.MEDIUM,
                assignee_id=1,
            )


    # Testet, ob die Priorität High korrekt als dringend gekennzeichnet ist.
    def test_priority_wird_korrekt_gesetzt(self):
        task = Task(
            id=1,
            title="Testaufgabe",
            priority=Priority.HIGH,
            assignee_id=1,
        )

        self.assertTrue(task.priority.is_urgent)

    # Testet, ob eine bereits erledigte Aufgabe trotz
    # überschrittener Deadline nicht als überfällig gilt.
    def test_erledigte_task_ist_nicht_ueberfaellig(self):
        task = Task(
            id=1,
            title="Testaufgabe",
            priority=Priority.MEDIUM,
            assignee_id=1,
            status=Status.DONE,
            due=datetime.now() - timedelta(days=1),
        )

        self.assertFalse(task.is_overdue(datetime.now()))

    # Erledigte Aufgaben sollen unabhängig von der Deadline
    # nicht als überfällig betrachtet werden.
    def test_offene_task_mit_vergangener_deadline_ist_ueberfaellig(self):
        task = Task(
            id=1,
            title="Testaufgabe",
            priority=Priority.MEDIUM,
            assignee_id=1,
            due=datetime.now() - timedelta(days=1),
        )

        self.assertTrue(task.is_overdue(datetime.now()))


if __name__ == "__main__":
    unittest.main()