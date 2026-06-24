# Django Frontend einrichten, aktuell halten und starten

Dieses Projekt verwendet `uv` als Paketmanager für das Django-Frontend.

Das Frontend läuft lokal auf Port `8001`.

Das Backend läuft separat und wird in dieser README nicht eingerichtet.

---

## 1. Voraussetzungen

Benötigt wird:

```text
Windows
PowerShell
uv
```

---

## 2. uv installieren

Falls `uv` noch nicht installiert ist, in PowerShell ausführen:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Danach PowerShell einmal schließen und neu öffnen.

Anschließend prüfen:

```powershell
uv --version
```

Wenn eine Versionsnummer angezeigt wird, ist `uv` installiert.

Alternative Installation über WinGet:

```powershell
winget install --id=astral-sh.uv -e
```

---

## 3. In den Frontend-Ordner wechseln

```powershell
cd C:\Zimmermann\Projekte\Python-WPF\Frontend
```

Alle weiteren Befehle werden im Frontend-Ordner ausgeführt.

---

## 4. Python-Version prüfen

Das Projekt verwendet die Python-Version aus der Datei:

```text
.python-version
```

Prüfen, welche Python-Version im Frontend verwendet wird:

```powershell
uv run python --version
```

Falls Python für das Projekt noch nicht installiert ist:

```powershell
uv python install
```

Danach erneut prüfen:

```powershell
uv run python --version
```

---

## 5. Frontend-Abhängigkeiten installieren

Beim ersten Einrichten des Projekts ausführen:

```powershell
uv sync
```

Dadurch erstellt `uv` die virtuelle Umgebung `.venv` und installiert alle Pakete aus:

```text
pyproject.toml
uv.lock
```

### Erstmalige Einrichtung (Manueller Download):

1. Lade das offizielle Tailwind-Windows-CLI-Executable herunter:
   **[Download-Link (Tailwind v4.3.1 Windows x64)](https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe)**
2. Benenne die heruntergeladene Datei in `tailwindcss.exe` um.
3. Kopiere die `tailwindcss.exe` direkt in diesen `Frontend/`-Ordner.

---

## 6. Frontend starten (inkl. Tailwind CSS v4 Build)

Das Projekt nutzt die offizielle, Node-freie **Tailwind Standalone CLI** für das CSS-Build-System. Du musst dafür kein Node.js, npm oder `package.json` installieren.

### Frontend starten:

Zum Starten des Frontends nutzen wir ein registriertes `uv`-Skript. Dieses prüft, ob die `tailwindcss.exe` da ist, gleicht leise die Version mit dem neuesten Release ab (und warnt bei Abweichungen), baut das CSS und startet den Django-Webserver auf Port `8001`:

**Standard-Start (für den Kunden / Deployment):**

Kompiliert das CSS einmalig frisch und startet den Django-Server (ohne Watch-Prozess im Hintergrund):
```powershell
uv run frontend
```

Danach ist das Frontend im Browser erreichbar unter:

```text
http://127.0.0.1:8001
```

---

## 7. Frontend stoppen

Den laufenden Django-Server stoppt man im PowerShell-Fenster mit:

```text
STRG + C
```

---

# Frontend aktuell halten

## 8. uv aktualisieren

Wenn `uv` über den PowerShell-Installer installiert wurde:

```powershell
uv self update
```

Danach prüfen:

```powershell
uv --version
```

Wenn `uv` über WinGet installiert wurde, dann über WinGet aktualisieren:

```powershell
winget upgrade --id=astral-sh.uv -e
```

---

## 9. Python-Version aktuell halten

Prüfen, welche Python-Version verwendet wird:

```powershell
uv run python --version
```

Installierte uv-Python-Versionen auf den neuesten Patchstand bringen:

```powershell
uv python upgrade
```

Danach erneut prüfen:

```powershell
uv run python --version
```

---

## 10. Prüfen, ob Pakete nicht mehr aktuell sind

Im Frontend-Ordner ausführen:

```powershell
uv pip list --outdated
```

Wenn Pakete angezeigt werden, gibt es neuere Versionen.

Wenn keine veralteten Pakete angezeigt werden, sind die installierten Pakete aktuell.

---

## 11. Abhängigkeiten aktualisieren

Alle Pakete innerhalb der erlaubten Versionsgrenzen aktualisieren:

```powershell
uv lock --upgrade
uv sync
```

Danach erneut prüfen:

```powershell
uv pip list --outdated
```

---

## 12. Einzelnes Paket aktualisieren

Beispiel für Django:

```powershell
uv lock --upgrade-package django
uv sync
```

Danach prüfen:

```powershell
uv run python -m django --version
```

---

## 13. Neues Paket hinzufügen

Beispiel:

```powershell
uv add requests
```

Dadurch wird das Paket in die `pyproject.toml` eingetragen und die `uv.lock` wird aktualisiert.

Danach kann das Frontend wie gewohnt gestartet werden:

```powershell
uv run python manage.py runserver 8001
```

---

# Wichtige Dateien

Diese Dateien gehören ins Git-Repository:

```text
pyproject.toml
uv.lock
.python-version
```

Dieser Ordner gehört nicht ins Git-Repository:

```text
.venv/
```

Falls `.venv/` noch nicht in der `.gitignore` steht, ergänzen:

```text
.venv/
```

---

# Kurzübersicht

uv installieren:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Frontend einrichten:
1. Lade das offizielle Tailwind-Windows-CLI-Executable herunter:
   **[Download-Link (Tailwind v4.3.1 Windows x64)](https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe)**
2. Benenne die heruntergeladene Datei in `tailwindcss.exe` um.
3. Kopiere die `tailwindcss.exe` direkt in diesen `Frontend/`-Ordner.

```powershell
cd C:\Zimmermann\Projekte\Python-WPF\Frontend
uv sync
```

Frontend starten:

```powershell
uv run frontend
```

Frontend öffnen:

```text
http://127.0.0.1:8001
```

Prüfen, ob Pakete veraltet sind:

```powershell
uv pip list --outdated
```

Pakete aktualisieren:

```powershell
uv lock --upgrade
uv sync
```
