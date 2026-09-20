# TaskMaster — Aufgabenverwaltung

Ein kleines Aufgabenverwaltungssystem in Python. Nutzer können Aufgaben anlegen,
bearbeiten, zuweisen, kategorisieren, nach Priorität sortieren und Berichte
generieren. Benachrichtigungen erfolgen per E-Mail (simuliert).

## Features

- Aufgaben anlegen, bearbeiten, löschen
- Nutzerverwaltung
- Prioritäten (1 = niedrig, 2 = mittel, 3 = hoch)
- Status-Workflow (neu → in Arbeit → erledigt)
- Benachrichtigungen per E-Mail, SMS und Push (simuliert)
- Berichte (Tages-, Wochen-, Monatsbericht)
- Einfache Datei-basierte Persistenz (JSON)

- neue Features: Tasksuche nach Parametern, statistische Auswertung der Tasks von Usern

## Starten

```bash
python main.py
```

## Projektstruktur

```
example-project/
├── main.py                # Einstiegspunkt
├── task_manager.py        # Zentrale Geschäftslogik
├── user.py                # Nutzerverwaltung
├── user_types.py          # Benutzertypen (User, AdminUser, ReadOnlyUser)
├── database.py            # Persistenz (JSON)
├── email_service.py       # E-Mail-Versand
├── notifications.py       # Benachrichtigungen
├── report_generator.py    # Berichte
├── utils.py               # Hilfsfunktionen
├── config.py              # Konfiguration
├── logger.py              # Logging
├── data/
│   ├── tasks.json
│   └── users.json
└── README.md
```
