import unittest

from taskmaster.infrastructure.notifiers import (
    SmtpNotifier,
    SmsNotifier,
    PushNotifier,
    CompositeNotifier,
    UrgentNotifier,
)


class FakeNotifier:

    # Speichert alle Aufrufe, damit im Test überprüft werden kann,
    # ob und wie oft der Notifier aufgerufen wurde.
    def __init__(self):
        self.calls = []

    # Simuliert das Versenden einer Benachrichtigung,
    # ohne tatsächlich eine Nachricht zu verschicken.
    def notify(self, recipient, subject, body):
        self.calls.append((recipient, subject, body))
        return True


class TestNotifiers(unittest.TestCase):

    # Testet, ob eine gültige E-Mail-Adresse vom SMTP-Notifier
    # akzeptiert und die Benachrichtigung erfolgreich verarbeitet wird.
    def test_smtp_notifier_akzeptiert_gueltige_email(self):
        notifier = SmtpNotifier(
            host="localhost",
            port=25,
            user="test",
            password="test",
        )

        recipient = {
            "email": "anna@example.com"
        }

        result = notifier.notify(
            recipient,
            "Test",
            "Testnachricht",
        )

        self.assertTrue(result)

    # Testet, ob eine ungültige E-Mail-Adresse korrekt abgelehnt wird.
    def test_smtp_notifier_lehnt_ungueltige_email_ab(self):
        notifier = SmtpNotifier(
            host="localhost",
            port=25,
            user="test",
            password="test",
        )

        recipient = {
            "email": "ungültig"
        }

        result = notifier.notify(
            recipient,
            "Test",
            "Testnachricht",
        )

        self.assertFalse(result)

    # Testet den CompositeNotifier.
    # Dabei wird überprüft, ob die Benachrichtigung an alle
    # enthaltenen Notifier weitergeleitet wird.
    def test_composite_notifier_ruft_alle_kanaele_auf(self):
        email = FakeNotifier()
        sms = FakeNotifier()

        notifier = CompositeNotifier([email, sms])

        recipient = {"email": "anna@example.com"}

        result = notifier.notify(
            recipient,
            "Test",
            "Nachricht",
        )

        self.assertTrue(result)
        self.assertEqual(len(email.calls), 1)
        self.assertEqual(len(sms.calls), 1)

    # Testet den UrgentNotifier.
    # Dabei wird überprüft, ob bei dringenden Benachrichtigungen
    # der Präfix "[DRINGEND]" automatisch ergänzt wird.
    def test_urgent_notifier_ergaenzt_praefix(self):
        inner = FakeNotifier()
        notifier = UrgentNotifier(inner)

        notifier.notify(
            {"email": "anna@example.com"},
            "Aufgabe",
            "Dringende Aufgabe",
        )

        self.assertEqual(
            inner.calls[0][1],
            "[DRINGEND] Aufgabe",
        )


if __name__ == "__main__":
    unittest.main()