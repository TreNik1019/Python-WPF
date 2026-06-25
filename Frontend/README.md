# Django Frontend einrichten, aktuell halten und starten

Dieses Projekt verwendet `uv` als Paketmanager für das Django-Frontend. Das Frontend
läuft lokal auf Port `8001`. Das Backend läuft separat und wird in dieser README nicht
eingerichtet.

## Voraussetzung

Benötigt wird _Windows_ mit _PowerShell_ sowie `uv` als Paketmanager.

## Installation von uv als Projektmanager

```shell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Danach PowerShell einmal schließen und neu öffnen und prüfen:

```shell
    uv --version
```

Alternative Installation über WinGet:

```shell
    winget install --id=astral-sh.uv -e
```

## In den Frontend-Ordner wechseln

```shell
    cd <Pfad-zu-deinem-Repo>\Python-WPF\Frontend
```

Alle weiteren Befehle werden im Frontend-Ordner ausgeführt.

## Python-Version prüfen

Das Projekt verwendet die Python-Version aus der Datei `.python-version`. Prüfen,
welche Python-Version im Frontend verwendet wird:

```shell
    uv run python --version
```

Falls Python für das Projekt noch nicht installiert ist:

```shell
    uv python install
```

## Tailwind CLI einrichten

Das Projekt nutzt die offizielle, Node-freie _Tailwind Standalone CLI_ für das
CSS-Build-System. Es wird dafür kein Node.js, npm oder `package.json` benötigt.

1. Lade das offizielle Tailwind-Windows-CLI-Executable herunter:
   **[Download-Link (Tailwind v4.3.1 Windows x64)](https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe)**
2. Benenne die heruntergeladene Datei in `tailwindcss.exe` um.
3. Kopiere die `tailwindcss.exe` direkt in diesen `Frontend`-Ordner.

## Abhängigkeiten installieren

```shell
    uv sync --all-groups
```

Dadurch erstellt `uv` die virtuelle Umgebung `.venv` und installiert alle Pakete aus
`pyproject.toml` und `uv.lock`, einschließlich der `lint`-Dependency-Group.

## Anwendung starten

Zum Starten des Frontends gibt es ein registriertes `uv`-Skript. Es prüft, ob die
`tailwindcss.exe` vorhanden ist, gleicht die lokale Version leise mit dem neuesten
Release ab (Warnung bei Abweichungen), baut das CSS einmalig frisch und startet
danach den Django-Webserver auf Port `8001`:

```shell
    uv run frontend
```

Danach ist das Frontend im Browser erreichbar unter `http://127.0.0.1:8001`.

## Anwendung stoppen

Den laufenden Django-Server stoppt man im PowerShell-Fenster mit `STRG + C`.

## Codeanalyse und Formatierung mit ruff

> Alle Befehle in diesem Abschnitt werden im `Frontend`-Ordner ausgeführt, damit
> nicht versehentlich der Backend-Code mit der Frontend-Umgebung geprüft wird.

Lint-Fehler anzeigen:

```shell
    uvx ruff check .
```

Lint-Fehler anzeigen und automatisch beheben, soweit möglich:

```shell
    uvx ruff check --fix .
```

Formatierung prüfen bzw. anwenden:

```shell
    uvx ruff format . --check
    uvx ruff format .
```

## Typprüfung mit ty

```shell
    uvx ty check .
```

## Sicherheitsanalyse mit pip-audit und PySentry

```shell
    uvx pip-audit
    uvx pysentry-rs
```

## uv aktuell halten

Wenn `uv` über den PowerShell-Installer installiert wurde:

```shell
    uv self update
```

Wenn `uv` über WinGet installiert wurde:

```shell
    winget upgrade --id=astral-sh.uv -e
```

## Python-Version aktuell halten

Installierte uv-Python-Versionen auf den neuesten Patchstand bringen:

```shell
    uv python upgrade
```

## Abhängigkeiten aktuell halten

Prüfen, ob Pakete nicht mehr aktuell sind:

```shell
    uv pip list --outdated
```

Alle Pakete innerhalb der erlaubten Versionsgrenzen aktualisieren:

```shell
    uv lock --upgrade
    uv sync
```

Einzelnes Paket aktualisieren, z. B. Django:

```shell
    uv lock --upgrade-package django
    uv sync
```

## Neues Paket hinzufügen

```shell
    uv add requests
```

Dadurch wird das Paket in die `pyproject.toml` eingetragen und die `uv.lock`
aktualisiert.

## Wichtige Dateien

Diese Dateien gehören ins Git-Repository:

```text
pyproject.toml
uv.lock
.python-version
```

Dieser Ordner gehört **nicht** ins Git-Repository und ist bereits in der `.gitignore`
ausgeschlossen:

```text
.venv/
```
