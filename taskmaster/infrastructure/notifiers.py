# SCHICHT: Infrastruktur — konkrete Zustellwege.
#
# Ersetzt email_service.py (EmailService) UND notifications.py (NotificationCenter).

from __future__ import annotations

import logging

from ..domain.ports import Notifier

log = logging.getLogger("taskmaster.notifiers")


# ---------------------------------------------------------------------------
# STRATEGY — ein Kanal, eine Klasse. Ersetzt die if channel==...-Kaskade.
# ---------------------------------------------------------------------------


class SmtpNotifier:
    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self._host = host
        self._port = port
        self._user = user
        self._password = password

    def notify(self, recipient: dict, subject: str, body: str) -> bool:
        to = recipient.get("email", "")
        if "@" not in to:
            log.error("Ungültige E-Mail: %r", to)
            return False
        if not subject or not body:
            log.error("Subject und Body dürfen nicht leer sein")
            return False
        log.info("MAIL -> %s | %s", to, subject)
        return True


class SmsNotifier:
    def notify(self, recipient: dict, subject: str, body: str) -> bool:
        number = recipient.get("phone", "")
        if len(number) < 5:
            log.error("Ungültige Telefonnummer: %r", number)
            return False
        log.info("SMS -> %s | %s: %s", number, subject, body)
        return True


class PushNotifier:
    def notify(self, recipient: dict, subject: str, body: str) -> bool:
        device = recipient.get("device", "")
        if not device:
            log.error("Kein Gerät hinterlegt")
            return False
        log.info("PUSH -> %s | %s: %s", device, subject, body)
        return True


# ---------------------------------------------------------------------------
# COMPOSITE — mehrere Kanäle hinter EINEM Port. Ersetzt "both" und "all".
# ---------------------------------------------------------------------------


class CompositeNotifier:
    def __init__(self, channels: list[Notifier]) -> None:
        self._channels = channels

    def notify(self, recipient: dict, subject: str, body: str) -> bool:
        results = [c.notify(recipient, subject, body) for c in self._channels]
        return all(results)


# ---------------------------------------------------------------------------
# DECORATOR — ergänzt das [DRINGEND]-Präfix. Ersetzt notify_urgent() vollständig.
# ---------------------------------------------------------------------------


class UrgentNotifier:
    PREFIX = "[DRINGEND]"

    def __init__(self, inner: Notifier) -> None:
        self._inner = inner

    def notify(self, recipient: dict, subject: str, body: str) -> bool:
        return self._inner.notify(recipient, f"{self.PREFIX} {subject}", body)