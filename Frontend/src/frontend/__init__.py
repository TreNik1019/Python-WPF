import sys
import os
import subprocess
import urllib.request
import re
from pathlib import Path


def main():
    # Set working directory to the Frontend folder (one level above src/frontend/)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    os.chdir(BASE_DIR)

    tailwindExe = BASE_DIR / "tailwindcss.exe"
    downloadUrl = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe"

    # 1. Prüfen, ob die tailwindcss.exe da ist
    if not tailwindExe.exists():
        print()
        print(
            "========================================================================="
        )
        print("\033[91mFEHLER: tailwindcss.exe nicht gefunden!\033[0m")
        print("Bitte lade die offizielle Standalone-CLI herunter und kopiere sie")
        print(f"als 'tailwindcss.exe' in diesen Ordner ({BASE_DIR}).")
        print()
        print("Download-Link (Windows x64):")
        print(downloadUrl)
        print(
            "========================================================================="
        )
        print()
        sys.exit(1)

    # 2. Version prüfen (Leise im Hintergrund)
    try:
        help_result = subprocess.run(
            [str(tailwindExe), "-h"], capture_output=True, text=True, check=True
        )
        help_text = help_result.stdout + help_result.stderr
        local_version_match = re.search(r"tailwindcss (v\d+\.\d+\.\d+)", help_text)

        if local_version_match:
            local_version = local_version_match.group(1)

            req = urllib.request.Request(
                "https://github.com/tailwindlabs/tailwindcss/releases/latest",
                method="HEAD",
            )
            with urllib.request.urlopen(req, timeout=3) as response:
                redirect_url = response.url
                latest_version_match = re.search(r"tag/(v\d+\.\d+\.\d+)", redirect_url)
                if latest_version_match:
                    latest_version = latest_version_match.group(1)
                    if local_version != latest_version:
                        print()
                        print(
                            "------------------------------------------------------------------------"
                        )
                        print(
                            f"\033[93mHINWEIS: Deine lokale Tailwind-Version ({local_version}) ist veraltet!\033[0m"
                        )
                        print(f"Die neueste Version ist: {latest_version}")
                        print(
                            "Falls Probleme auftreten, kannst du die neue Version hier laden:"
                        )
                        print(downloadUrl)
                        print(
                            "------------------------------------------------------------------------"
                        )
                        print()
    except Exception:
        pass

    # 3. Einmalig CSS kompilieren
    print("Kompiliere CSS mit Tailwind CSS v4...")
    subprocess.run(
        [str(tailwindExe), "-i", "static/css/index.css", "-o", "static/css/main.css"],
        check=True,
    )

    # 4. Django starten
    venv_python = BASE_DIR / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        venv_python = BASE_DIR / ".venv" / "bin" / "python"

    python_executable = str(venv_python) if venv_python.exists() else sys.executable

    try:
        print("Starte Django Webserver...")
        subprocess.run([python_executable, "manage.py", "runserver", "8001"])
    except KeyboardInterrupt:
        print("\nDjango Webserver wird beendet...")
