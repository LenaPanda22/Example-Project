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

## Tests

```bash
python -m unittest discover -s tests -v
```

## Projektstruktur

```
example-project/
├── data/
│   ├── tasks.json
│   └── users.json
├── doku/
│   ├── todo
│   └── todo
├── legacy/                # Alte Dateien
├── taskmaster/
│   ├── application/       # Zentrale Geschäftslogik
│   ├── domain/            # Entitäten und Ports
│   └── infrastructure/    # Infrastruktur
├── tests/                 # Tests
├── main.py                # Einstiegspunkt
└── README.md
```
