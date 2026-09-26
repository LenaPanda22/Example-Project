import unittest
from datetime import datetime, timedelta

from taskmaster.application.task_service import TaskService
from taskmaster.application.statistic_service import StatisticsService

class InMemoryTaskRepository:

    def __init__(self):
        self._tasks = {}

    def save(self, task):
        self._tasks[task["id"]] = task
        return True

    def get(self, task_id):
        return self._tasks.get(task_id)

    def delete(self, task_id):
        self._tasks.pop(task_id, None)

    def get_all(self):
        return self._tasks


class FakeNotificationService:

    def __init__(self):
        self.new_task_calls = []
        self.done_calls = []

    def send_new_task_notification(self, assignee_id, priority, title):
        self.new_task_calls.append((assignee_id, priority, title))
        return True

    def send_done_notification(self, task):
        self.done_calls.append(task)
        return True


# Kernlogik-Test 1: TaskService gegen gemockte Infrastruktur

class TestTaskServiceCoreLogic(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryTaskRepository()
        self.notifier = FakeNotificationService()
        self.service = TaskService(self.repo, self.notifier)

    # Eine gültige Aufgabe wird gespeichert und löst genau eine
    # Benachrichtigung aus.
    def test_create_task_speichert_und_benachrichtigt(self):
        ok = self.service.create_task(1, "Testaufgabe", "Beschreibung", 2, 42)

        self.assertTrue(ok)
        self.assertIsNotNone(self.repo.get(1))
        self.assertEqual(len(self.notifier.new_task_calls), 1)
        self.assertEqual(self.notifier.new_task_calls[0][0], 42)  # assignee_id

    # Ein leerer Titel wird abgelehnt, es wird nichts gespeichert und
    # keine Benachrichtigung ausgelöst.
    def test_create_task_lehnt_leeren_titel_ab(self):
        ok = self.service.create_task(2, "", "Beschreibung", 2, 42)

        self.assertFalse(ok)
        self.assertIsNone(self.repo.get(2))
        self.assertEqual(len(self.notifier.new_task_calls), 0)

    # Eine ungültige Priorität wird abgelehnt.
    def test_create_task_lehnt_ungueltige_prioritaet_ab(self):
        ok = self.service.create_task(3, "Titel", "Beschreibung", 9, 42)

        self.assertFalse(ok)
        self.assertIsNone(self.repo.get(3))

    # Wird eine Aufgabe auf "done" gesetzt, löst das eine
    # Erledigt-Benachrichtigung aus.
    def test_update_status_done_benachrichtigt(self):
        self.service.create_task(4, "Titel", "Beschreibung", 1, 42)

        ok = self.service.update_status(4, "done")

        self.assertTrue(ok)
        self.assertEqual(self.repo.get(4)["status"], "done")
        self.assertEqual(len(self.notifier.done_calls), 1)

    # Ein unbekannter Status wird abgelehnt.
    def test_update_status_lehnt_unbekannten_status_ab(self):
        self.service.create_task(5, "Titel", "Beschreibung", 1, 42)

        ok = self.service.update_status(5, "völlig_unbekannt")

        self.assertFalse(ok)
        self.assertEqual(self.repo.get(5)["status"], "new")

# Kernlogik-Test 2: StatisticsService (neues Feature) gegen gemockte Infrastruktur

class TestStatisticsServiceFeature(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryTaskRepository()
        self.service = StatisticsService(self.repo)

        gestern = (datetime.now() - timedelta(days=1)).isoformat()
        morgen = (datetime.now() + timedelta(days=1)).isoformat()

        # Nutzer 1: 3 Aufgaben (1 done, 1 offen überfällig, 1 offen zukünftig)
        self.repo.save({"id": 1, "assignee": 1, "status": "done", "due": gestern, "title": "a"})
        self.repo.save({"id": 2, "assignee": 1, "status": "new", "due": gestern, "title": "b"})
        self.repo.save({"id": 3, "assignee": 1, "status": "in_progress", "due": morgen, "title": "c"})
        # Nutzer 2: 1 Aufgabe (soll die Statistik von Nutzer 1 nicht beeinflussen)
        self.repo.save({"id": 4, "assignee": 2, "status": "new", "due": gestern, "title": "d"})

    # Zählt nur die Aufgaben des angefragten Nutzers.
    def test_zaehlt_nur_eigene_aufgaben(self):
        stats = self.service.user_statistics(1)

        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["done"], 1)

    # Eine offene Aufgabe mit vergangener Deadline zählt als überfällig,
    # eine erledigte oder zukünftige nicht.
    def test_ueberfaellig_wird_korrekt_gezaehlt(self):
        stats = self.service.user_statistics(1)

        self.assertEqual(stats["overdue"], 1)  # nur Aufgabe 2

    # Ein Nutzer ohne Aufgaben liefert eine leere Statistik ohne Fehler.
    def test_nutzer_ohne_aufgaben(self):
        stats = self.service.user_statistics(999)

        self.assertEqual(stats["total"], 0)
        self.assertEqual(stats["overdue"], 0)


if __name__ == "__main__":
    unittest.main()
