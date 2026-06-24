# Python-WPF – Patientenverwaltungssystem

## Projektübersicht

Dieses Projekt ist ein modernes Patientenverwaltungssystem, das im Rahmen eines Hochschulprojekts (Hochschule Karlsruhe) entwickelt wurde. Es demonstriert eine produktionsnahe Python-Webanwendung mit sauber getrennten Schichten und aktuellen Best Practices.

---

## Architektur

Das System besteht aus zwei unabhängigen Anwendungen:

| Komponente | Framework     | Beschreibung                         |
|------------|---------------|--------------------------------------|
| Backend    | FastAPI       | REST- und GraphQL-API, ASGI          |
| Frontend   | Django 6.0+   | Weboberfläche für die Patientenverwaltung |

### Schichtenarchitektur (Backend)

```
Router (HTTP / GraphQL)
    └── Service (Geschäftslogik)
            └── Repository (Datenzugriff)
                    └── Entity (Domänenobjekte)
```

---

## Technologie-Stack

### Backend
- **FastAPI** – ASGI-Framework für REST und GraphQL
- **SQLAlchemy 2** – ORM für PostgreSQL
- **Strawberry GraphQL** – GraphQL-Schema und -Resolver
- **Pydantic v2** – Validierung und Serialisierung
- **Keycloak** – OAuth2/OIDC-Authentifizierung
- **Loguru** – Logging
- **Prometheus** – Metriken und Monitoring
- **uv** – Paket- und Projektverwaltung
- **Ruff** – Linting und Formatierung
- **pytest** – Unit- und Integrationstests
- **Locust** – Lasttests

### Frontend
- **Django 6.0+** – Webframework
- **SQLite** – Datenbank (Entwicklung)
- **django-environ** – Umgebungsvariablen via `.env`

### Infrastruktur
- **PostgreSQL** – Produktionsdatenbank
- **Docker / Docker Compose** – Containerisierung
- **SonarQube** – Codeanalyse

---

## Projektstruktur

```
Python-WPF/
├── Backend/               # FastAPI-Backend
│   ├── src/patient/       # Hauptpaket
│   │   ├── entity/        # Domänenobjekte (Patient, Adresse, Rechnung, …)
│   │   ├── repository/    # Datenzugriff
│   │   ├── service/       # Geschäftslogik
│   │   └── router/        # HTTP-Endpunkte und GraphQL
│   ├── tests/             # Unit- und Integrationstests
│   ├── docs/              # MkDocs-Dokumentation
│   └── pyproject.toml     # Abhängigkeiten und Build-Konfiguration
├── Frontend/              # Django-Frontend
│   ├── patient/           # Django-App
│   ├── templates/         # HTML-Templates
│   └── config/            # Django-Einstellungen
├── extras/                # Postman-Collection, Locust, Skripte
└── .gitignore
```

---

## Domänenmodell

| Entity          | Beschreibung                    |
|-----------------|---------------------------------|
| `Patient`       | Kernentität mit Personendaten   |
| `Adresse`       | Adresse eines Patienten         |
| `Rechnung`      | Abrechnung zugeordnet zu Patient |
| `Facharzt`      | Behandelnder Facharzt           |
| `Geschlecht`    | Enum: biologisches Geschlecht   |
| `Familienstand` | Enum: Familienstand             |

---

## API

### REST-Endpunkte (Backend)

| Methode  | Pfad                  | Beschreibung               |
|----------|-----------------------|----------------------------|
| `GET`    | `/patient`            | Alle Patienten (paginiert) |
| `GET`    | `/patient/{id}`       | Patient nach ID            |
| `POST`   | `/patient`            | Neuen Patienten anlegen    |
| `PUT`    | `/patient/{id}`       | Patienten aktualisieren    |
| `DELETE` | `/patient/{id}`       | Patienten löschen          |
| `GET`    | `/health`             | Health-Check               |

### GraphQL

GraphQL-Endpunkt unter `/graphql` – unterstützt Queries und Mutations für das Patientenmodell.

---

## Setup & Installation

Detaillierte Installationsanleitungen befinden sich in:
- `Backend/README.install.md` – Windows-11-Installationsanleitung
- `Backend/installationsanleitung.md` – Ausführliche Anleitung (Deutsch)

### Schnellstart Backend

```bash
cd Backend
uv sync
uv run python -m patient
```

### Schnellstart Frontend

```powershell
cd Frontend
uv sync
uv run frontend
```

Das registrierte `uv`-Skript `frontend` baut das Tailwind-CSS und startet den Django-Entwicklungsserver auf Port **8001**. Details siehe `Frontend/README.md`.

---

## Tests

```bash
cd Backend

# Unit-Tests
uv run pytest tests/unit

# Integrationstests
uv run pytest tests/integration

# Mit Coverage-Report
uv run pytest --cov=src --cov-report=html
```

---

## Authentifizierung

Das Backend nutzt **Keycloak** als Identity Provider (OAuth2/OIDC). Im Entwicklungsmodus kann die Authentifizierung über `dev_modus.py` deaktiviert werden.

---

## Lizenz

GPL-3.0-or-later
