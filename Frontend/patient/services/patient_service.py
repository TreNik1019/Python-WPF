"""Utilities to build a mock patient dataset from CSV files.

This module reads patient and address CSV files (semicolon-delimited)
and exposes a simple `get_all` function that supports filtering and
pagination. It builds `MOCK_PATIENTEN` at import time.

"""

import csv
import json
import math
from pathlib import Path

# Build paths to CSV files relative to this file
BASE_DIR = Path(__file__).resolve().parent
BASE_CSV_DIR = (
    BASE_DIR
    .joinpath(
        "../../../../extras/compose/postgres/init/patient/csv",
    )
    .resolve()
)

_PATIENT_CSV = BASE_CSV_DIR / "patient.csv"
_ADRESSE_CSV = BASE_CSV_DIR / "adresse.csv"


def _read_adressen(path: Path) -> dict[int, dict[str, str]]:
    """Read addresses CSV and return a mapping patient_id -> address.

    Only the file opening is wrapped in a try-block to keep the block
    small; per-row parsing handles conversion errors locally.
    """
    adressen = {}
    try:
        fh = path.open(newline="", encoding="utf-8")
    except FileNotFoundError:
        return adressen

    with fh:
        reader = csv.DictReader(fh, delimiter=";")
        for row in reader:
            try:
                pid = int(row.get("patient_id") or 0)
            except ValueError:
                # skip malformed id
                continue
            adressen[pid] = {
                "plz": row.get("plz", ""),
                "ort": row.get("ort", ""),
            }
    return adressen


def _parse_int(value: object, default: int = 0) -> int:
    try:
        return int(str(value))
    except (ValueError, TypeError):
        return default


def _parse_fachaerzte(fach_raw: str | None) -> list[str]:
    """Parse the fachaerzte field into a list of strings.

    Returns an empty list for null/empty values.
    """
    if fach_raw is None:
        return []
    fach_str = fach_raw.strip()
    if not fach_str or fach_str.lower() == "null":
        return []
    try:
        parsed = json.loads(fach_str)
    except (ValueError, KeyError):
        return []
    return [str(x) for x in parsed]


def _read_patienten(
    path: Path,
    adressen: dict[int, dict[str, str]],
) -> list[dict[str, object]]:
    """Read patients CSV and return list of patient dicts.

    The file opening is isolated in a small try-block; per-row parsing
    handles conversion errors locally.
    """
    patients = []

    def _row_to_patient(
        row: dict[str, str],
        adressen_map: dict[int, dict[str, str]],
    ) -> dict[str, object]:
        pid = _parse_int(row.get("id"), 0)
        if pid == 0:
            return {}

        nachname = row.get("nachname", "")
        email = row.get("email", "")
        kategorie = _parse_int(row.get("kategorie"), 0)

        has_newsletter = str(row.get("has_newsletter", "")).strip().lower() == "true"
        geburtsdatum = row.get("geburtsdatum", "")
        homepage = row.get("homepage", "")
        geschlecht = row.get("geschlecht", "")
        familienstand = row.get("familienstand", "")

        fachaerzte = _parse_fachaerzte(row.get("fachaerzte"))

        username = row.get("username", "")

        adresse = adressen_map.get(pid, {"plz": "", "ort": ""})

        return {
            "id": pid,
            "nachname": nachname,
            "email": email,
            "kategorie": kategorie,
            "has_newsletter": has_newsletter,
            "geburtsdatum": geburtsdatum,
            "homepage": homepage,
            "geschlecht": geschlecht,
            "familienstand": familienstand,
            "adresse": {
                "plz": adresse.get("plz", ""),
                "ort": adresse.get("ort", ""),
            },
            "fachaerzte": fachaerzte,
            "username": username,
        }

    try:
        fh = path.open(newline="", encoding="utf-8")
    except FileNotFoundError:
        return patients

    with fh:
        reader = csv.DictReader(fh, delimiter=";")
        for row in reader:
            obj = _row_to_patient(row, adressen)
            if obj:
                patients.append(obj)

    return patients


# Build MOCK_PATIENTEN at import time
_ADRESSEN = _read_adressen(_ADRESSE_CSV)
MOCK_PATIENTEN = _read_patienten(_PATIENT_CSV, _ADRESSEN)


def get_all(
    nachname: str | None = None,
    email: str | None = None,
    page: int = 0,
    size: int = 5,
) -> dict[str, object]:
    """Return filtered and paginated patients.

    Args:
        nachname: optional partial match for last name (case-insensitive)
        email: optional partial match for email (case-insensitive)
        page: page number (0-based)
        size: page size

    Returns:
        dict with keys 'content' and 'page' as specified.

    """
    results = list(MOCK_PATIENTEN)

    if nachname and isinstance(nachname, str):
        results = [
            p
            for p in results
            if nachname.lower() in str(p.get("nachname") or "").lower()
        ]

    if email and isinstance(email, str):
        results = [
            p
            for p in results
            if email.lower() in str(p.get("email") or "").lower()
        ]

    total_elements = len(results)

    if size is None:
        size = 5
    try:
        size = int(size)
    except (ValueError, TypeError):
        size = 5
    if size <= 0:
        size = total_elements if total_elements > 0 else 1

    total_pages = math.ceil(total_elements / size) if size > 0 else 0

    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 0
    page = max(page, 0)

    start = page * size
    end = start + size
    content = results[start:end]

    return {
        "content": content,
        "page": {
            "size": size,
            "number": page,
            "total_elements": total_elements,
            "total_pages": total_pages,
        },
    }
