# SCHICHT: Domain

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum

class DomainError(Exception):
    """Fachlicher Fehler (z. B. ungueltiger Task). Kein Infrastruktur-Fehler."""

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @property
    def label(self) -> str:
        return _PRIORITY_LABELS[self]

    @property
    def is_urgent(self) -> bool:
        return self is Priority.HIGH


_PRIORITY_LABELS = {
    Priority.LOW: "niedrig",
    Priority.MEDIUM: "mittel",
    Priority.HIGH: "hoch",
}


class Status(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"

    @property
    def label(self) -> str:
        return _STATUS_LABELS[self]

    @property
    def is_closed(self) -> bool:
        return self in (Status.DONE, Status.CANCELLED)


_STATUS_LABELS = {
    Status.NEW: "Neu",
    Status.IN_PROGRESS: "In Arbeit",
    Status.DONE: "Erledigt",
    Status.CANCELLED: "Abgebrochen",
}


@dataclass
class Task:
    id: int
    title: str
    priority: Priority
    assignee_id: int
    description: str = ""
    status: Status = Status.NEW
    due: datetime | None = None
    created: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.title:
            raise DomainError("Titel darf nicht leer sein")
        self.priority = Priority(self.priority)
        self.status = Status(self.status)

    def is_overdue(self, now: datetime) -> bool:
        if self.due is None or self.status.is_closed:
            return False
        return self.due < now

    def change_status(self, new_status: Status) -> None:
        self.status = Status(new_status)

    @property
    def display(self) -> str:
        """Ersetzt TaskManager.format_task()."""
        return f"#{self.id} {self.title} [{self.priority.label}] ({self.status.label})"