# SCHICHT: Domain — Ports (Schnittstellen)

from __future__ import annotations

from typing import Protocol


class Notifier(Protocol):
    def notify(self, recipient: dict, subject: str, body: str) -> bool: ...


# Hinweis: TaskRepository / UserRepository gehoeren zu Vorschlag 1 & 3
# (Aufteilung + Composition Root) und werden dort ergaenzt.