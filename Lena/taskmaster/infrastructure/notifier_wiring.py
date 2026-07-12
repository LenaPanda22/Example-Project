from __future__ import annotations

from ..domain.ports import Notifier
from ..domain.task import Priority
from .notifiers import CompositeNotifier, UrgentNotifier


def build_escalation(
    email: Notifier, sms: Notifier, push: Notifier
) -> dict[Priority, Notifier]:
    return {
        Priority.LOW: email,
        Priority.MEDIUM: CompositeNotifier([email, sms]),
        Priority.HIGH: UrgentNotifier(CompositeNotifier([email, sms, push])),
    }