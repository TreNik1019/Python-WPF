"""Skript, um Frontend-Assets zu pruefen und den Django-Server zu starten."""

import json
import os
import re
import subprocess  # noqa: S404
import sys
import urllib.parse
import urllib.request
from pathlib import Path

DOWNLOAD_URL = (
    "https://github.com/tailwindlabs/tailwindcss/releases/latest"
    "/download/tailwindcss-windows-x64.exe"
)
LUCIDE_PACKAGE_URL = "https://unpkg.com/lucide@latest/package.json"
LUCIDE_LATEST_DOWNLOAD_URL = "https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"
LUCIDE_DOWNLOAD_URL_TEMPLATE = (
    "https://unpkg.com/lucide@{version}/dist/umd/lucide.min.js"
)
UPDATE_LUCIDE_ENV = "UPDATE_LUCIDE"


def _assert_lucide_download_url(download_url: str) -> None:
    """Erlaubt Lucide-Downloads nur per HTTPS von unpkg.com."""
    parsed_url = urllib.parse.urlparse(download_url)
    if parsed_url.scheme != "https" or parsed_url.netloc != "unpkg.com":
        raise RuntimeError("Ungueltige Lucide-Download-URL.")


def _check_tailwind_version(tailwind_exe: Path) -> None:
    """Vergleicht lokale mit neuester Tailwind-Version und warnt bei Abweichung."""
    help_result = subprocess.run(  # noqa: S603
        [str(tailwind_exe), "-h"], capture_output=True, text=True, check=True
    )
    help_text = help_result.stdout + help_result.stderr
    local_version_match = re.search(r"tailwindcss (v\d+\.\d+\.\d+)", help_text)
    if not local_version_match:
        return

    local_version = local_version_match.group(1)
    req = urllib.request.Request(
        "https://github.com/tailwindlabs/tailwindcss/releases/latest",
        method="HEAD",
    )
    # feste https-URL zu github.com, kein nutzergesteuertes Schema
    with urllib.request.urlopen(req, timeout=3) as response:  # noqa: S310
        latest_version_match = re.search(r"tag/(v\d+\.\d+\.\d+)", response.url)

    if not latest_version_match:
        return

    latest_version = latest_version_match.group(1)
    if local_version == latest_version:
        return

    print()
    print("-" * 74)
    print(
        f"\033[93mHINWEIS: Deine lokale Tailwind-Version ({local_version}) "
        "ist veraltet!\033[0m"
    )
    print(f"Die neueste Version ist: {latest_version}")
    print("Falls Probleme auftreten, kannst du die neue Version hier laden:")
    print(DOWNLOAD_URL)
    print("-" * 74)
    print()


def _fetch_lucide_latest_version() -> str | None:
    """Liest die neueste Lucide-Version aus dem Package-Metadaten-Endpunkt."""
    req = urllib.request.Request(LUCIDE_PACKAGE_URL, method="GET")
    # feste https-URL zu unpkg.com, kein nutzergesteuertes Schema
    with urllib.request.urlopen(req, timeout=5) as response:  # noqa: S310
        metadata = json.loads(response.read().decode("utf-8"))
    version = metadata.get("version")
    return version if isinstance(version, str) else None


def _download_lucide(lucide_file: Path, version_file: Path, version: str) -> None:
    """Laedt die Lucide-UMD-Datei lokal in den static-Ordner."""
    lucide_file.parent.mkdir(parents=True, exist_ok=True)
    download_url = LUCIDE_DOWNLOAD_URL_TEMPLATE.format(version=version)
    _assert_lucide_download_url(download_url)
    # feste https-URL zu unpkg.com, Version kommt aus Lucide-package.json
    req = urllib.request.Request(download_url, method="GET")  # noqa: S310
    with urllib.request.urlopen(req, timeout=10) as response:  # noqa: S310
        lucide_file.write_bytes(response.read())
    version_file.write_text(version, encoding="utf-8")


def _ensure_lucide(base_dir: Path) -> None:
    """Stellt sicher, dass Lucide lokal vorhanden ist, und warnt bei Updates."""
    lucide_file = base_dir / "static" / "js" / "lucide.min.js"
    version_file = base_dir / "static" / "js" / "lucide.version"
    should_update = os.environ.get(UPDATE_LUCIDE_ENV) == "1"

    if not lucide_file.exists():
        latest_version = _fetch_lucide_latest_version()
        if latest_version is None:
            raise RuntimeError("Lucide-Version konnte nicht ermittelt werden.")
        _download_lucide(lucide_file, version_file, latest_version)
        print(f"Lucide lokal installiert: {latest_version}")
        return

    latest_version = _fetch_lucide_latest_version()
    if latest_version is None:
        return

    local_version = (
        version_file.read_text(encoding="utf-8").strip()
        if version_file.exists()
        else "unbekannt"
    )

    if local_version == latest_version:
        return

    if should_update:
        _download_lucide(lucide_file, version_file, latest_version)
        print(f"Lucide aktualisiert: {local_version} -> {latest_version}")
        return

    print()
    print("-" * 74)
    print(
        f"\033[93mHINWEIS: Deine lokale Lucide-Version ({local_version}) "
        "ist veraltet!\033[0m"
    )
    print(f"Die neueste Version ist: {latest_version}")
    print("Download-Link:")
    print(LUCIDE_LATEST_DOWNLOAD_URL)
    print("Automatisch aktualisieren:")
    print(f"    $env:{UPDATE_LUCIDE_ENV}='1'; uv run frontend")
    print("-" * 74)
    print()


def main() -> None:
    """Baut das CSS mit Tailwind und startet den Django-Webserver auf Port 8001."""
    base_dir = Path(__file__).resolve().parent
    os.chdir(base_dir)

    tailwind_exe = base_dir / "tailwindcss.exe"

    # 1. Prüfen, ob die tailwindcss.exe da ist
    if not tailwind_exe.exists():
        print()
        print("=" * 73)
        print("\033[91mFEHLER: tailwindcss.exe nicht gefunden!\033[0m")
        print("Bitte lade die offizielle Standalone-CLI herunter und kopiere sie")
        print(f"als 'tailwindcss.exe' in diesen Ordner ({base_dir}).")
        print()
        print("Download-Link (Windows x64):")
        print(DOWNLOAD_URL)
        print("=" * 73)
        print()
        sys.exit(1)

    # 2. Version prüfen (leise im Hintergrund, Fehler werden ignoriert)
    try:
        _check_tailwind_version(tailwind_exe)
    except (subprocess.SubprocessError, OSError) as exc:
        print(f"Hinweis: Tailwind-Versionsprüfung übersprungen ({exc}).")

    # 3. Lucide lokal bereitstellen und ggf. Version pruefen
    try:
        _ensure_lucide(base_dir)
    except (OSError, RuntimeError) as exc:
        print(f"Hinweis: Lucide-Prüfung übersprungen ({exc}).")

    # 4. Einmalig CSS kompilieren
    print("Kompiliere CSS mit Tailwind CSS v4...")
    subprocess.run(  # noqa: S603
        [str(tailwind_exe), "-i", "static/css/index.css", "-o", "static/css/main.css"],
        check=True,
    )

    # 5. Django starten
    venv_python = base_dir / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        venv_python = base_dir / ".venv" / "bin" / "python"

    python_executable = str(venv_python) if venv_python.exists() else sys.executable

    try:
        print("Starte Django Webserver...")
        subprocess.run(  # noqa: S603
            [python_executable, "manage.py", "runserver", "8001"], check=False
        )
    except KeyboardInterrupt:
        print("\nDjango Webserver wird beendet...")


if __name__ == "__main__":
    main()
