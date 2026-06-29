# Frontend-Erklaerung

Das Frontend ist eine kleine Django-Webanwendung fuer die Patientenverwaltung. Es
stellt die Suchoberflaeche bereit, nimmt Benutzereingaben entgegen und ruft das
FastAPI-Backend ab. Die Patientendaten werden nicht direkt im Frontend gespeichert,
sondern ueber die REST-Schnittstelle des Backends geladen.

## Verwendete Technologien

| Technologie | Einsatz im Frontend |
| --- | --- |
| Python 3.14 | Programmiersprache fuer Django, Startskript und Backend-Zugriffe |
| Django 6 | Webframework fuer Routing, Views, Templates und statische Dateien |
| uv | Projektverwaltung, Installation der Abhaengigkeiten und Start von `frontend` |
| httpx | HTTP-Client fuer die Verbindung vom Frontend zum Backend |
| Tailwind CSS Standalone CLI | Erzeugt die CSS-Datei `static/css/main.css` ohne Node.js/npm |
| Lucide | Icon-Bibliothek, lokal eingebunden ueber `static/js/lucide.min.js` |
| django-environ | Liest Einstellungen aus Umgebungsvariablen bzw. `.env` |
| Ruff und ty | Codeanalyse, Formatierung und Typpruefung |

## Aufbau

| Bereich | Datei/Ordner | Aufgabe |
| --- | --- | --- |
| Startskript | `frontend.py` | Prueft Tailwind und Lucide, baut CSS und startet Django auf Port 8001 |
| Django-Konfiguration | `config/settings.py` | Konfiguriert Apps, Templates, Static Files, CSP, Backend-URL und Logging |
| URL-Konfiguration | `config/urls.py`, `patient/urls.py` | Verknuepft Browser-URLs mit den Django-Views |
| Views | `patient/views.py` | Verarbeitet Suchanfragen, validiert Eingaben und bereitet Template-Daten vor |
| Backend-Service | `patient/services/patient_service.py` | Kapselt HTTP-Aufrufe an das FastAPI-Backend |
| Templates | `templates/` | Enthalten HTML-Grundlayout und Suchseite |
| Statische Dateien | `static/` | CSS, Logo und lokale JavaScript-Dateien |

## Verbindung Zum Backend

Die Backend-Adresse steht in `config/settings.py`:

```python
BACKEND_URL = env("BACKEND_URL", default="https://127.0.0.1:8000/rest")
```

Dadurch kann die URL lokal ueber eine `.env`-Datei oder Umgebungsvariable
ueberschrieben werden. Die TLS-Pruefung ist ebenfalls konfigurierbar:

```python
BACKEND_TLS_VERIFY = env.bool("BACKEND_TLS_VERIFY", default=not DEBUG)
```

Im Frontend ruft `patient_service.py` das Backend mit `httpx` auf. Die Funktionen
kapseln die konkreten REST-Aufrufe:

| Funktion | Zweck |
| --- | --- |
| `get_all_html()` | Holt eine HTML-Tabelle fuer die aktuelle Suchseite |
| `get_count()` | Holt per JSON die Gesamtanzahl der Treffer fuer die Pagination |
| `get_by_id_html()` | Holt die Detailansicht eines einzelnen Patienten als HTML |

## Datenfluss

1. Der Benutzer oeffnet die Suchseite und gibt eine ID oder einen Nachnamen ein.
2. `search_view()` in `patient/views.py` liest die Query-Parameter aus.
3. Die Eingabe wird validiert, damit nur erlaubte Zeichen verarbeitet werden.
4. Je nach Suche ruft die View den Backend-Service auf.
5. `patient_service.py` sendet den HTTP-Request an das FastAPI-Backend.
6. Das Backend liefert fuer die Anzeige HTML zurueck.
7. Die View legt das HTML und Metadaten wie Trefferzahl, aktuelle Seite und Filtertyp in den Template-Kontext.
8. `templates/patient/search.html` rendert die Suchoberflaeche und bindet den Ergebnisbereich ein.

## Darstellung Der Daten

Das Backend liefert die Patiententabelle bereits als HTML. Das Frontend uebernimmt
diesen HTML-Block und setzt ihn in den Ergebnisbereich der Suchseite ein. Die
Formatierung der Tabelle passiert ueber Tailwind-Klassen im Template.

Bei der ID-Suche liefert das Backend eine einzelne HTML-Detailansicht. Das
Frontend liest daraus die relevanten Felder aus und stellt sie in derselben
Tabellenstruktur dar wie die normale Suche.

Die Pagination wird im Frontend verwaltet. Dafuer fragt das Frontend zusaetzlich
die Gesamtanzahl der Treffer ab und berechnet daraus, ob es eine naechste Seite
gibt.

## Statische Assets

Tailwind und Lucide werden lokal betrieben:

| Asset | Verwaltung |
| --- | --- |
| `tailwindcss.exe` | Liegt im Frontend-Ordner und wird beim Start auf neue Versionen geprueft |
| `static/css/main.css` | Wird beim Start mit Tailwind neu gebaut |
| `static/js/lucide.min.js` | Wird lokal geladen; bei fehlender Datei automatisch heruntergeladen |
| `static/js/lucide.version` | Speichert die lokal installierte Lucide-Version |
| `static/js/app.js` | Initialisiert die Lucide-Icons im Browser |

Durch die lokale Einbindung von Lucide braucht die laufende Webseite kein externes
CDN. Deshalb kann die Content Security Policy fuer Skripte restriktiv bleiben:

```python
"script-src": ["'self'"]
```

## Start Des Frontends

Das Frontend wird im Ordner `Frontend` gestartet:

```shell
uv run frontend
```

Dabei passiert automatisch:

1. Tailwind-Version pruefen.
2. Lucide lokal bereitstellen bzw. Version pruefen.
3. CSS mit Tailwind bauen.
4. Django-Entwicklungsserver auf Port 8001 starten.
