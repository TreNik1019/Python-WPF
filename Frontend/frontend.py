"""Skript, um Tailwind CSS zu bauen und den Django-Entwicklungsserver zu starten."""

import os
import re
import subprocess  # noqa: S404
import sys
import urllib.request
from pathlib import Path

DOWNLOAD_URL = (
    "https://github.com/tailwindlabs/tailwindcss/releases/latest"
    "/download/tailwindcss-windows-x64.exe"
)


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

    # 3. Einmalig CSS kompilieren
    print("Kompiliere CSS mit Tailwind CSS v4...")
    subprocess.run(  # noqa: S603
        [str(tailwind_exe), "-i", "static/css/index.css", "-o", "static/css/main.css"],
        check=True,
    )

    # 4. Django starten
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
