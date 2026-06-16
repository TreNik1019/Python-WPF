"""Mock-Repository fuer Patientendaten ohne Datenbank."""

from collections.abc import Mapping, Sequence
from datetime import date
from typing import Any, Final

from patient.entity import Adresse, Facharzt, Familienstand, Geschlecht, Patient
from patient.repository.pageable import Pageable
from patient.repository.slice import Slice

__all__ = ["PatientMockRepository"]


class PatientMockRepository:
    """Mock-Repository fuer Patientendaten."""

    def __init__(self) -> None:
        """Initialisiert feste Mockdaten."""
        self.patienten: Final = (
            self._create_patient(1, "Alpha", "alpha@acme.de", "admin", "76131"),
            self._create_patient(20, "Beta", "beta@acme.de", "patient", "76133"),
            self._create_patient(30, "Gamma", "gamma@acme.de", "patient30", "76135"),
            self._create_patient(50, "Delta", "delta@acme.de", "patient50", "76137"),
            self._create_patient(
                60, "Epsilon", "epsilon@acme.de", "patient60", "76139"
            ),
            self._create_patient(70, "Zeta", "zeta@acme.de", "patient70", "76141"),
            self._create_patient(80, "Eta", "eta@acme.de", "patient80", "76143"),
            self._create_patient(90, "Theta", "theta@acme.de", "patient90", "76145"),
            self._create_patient(100, "Iota", "iota@acme.de", "patient100", "76147"),
            self._create_patient(
                110, "Kappa", "kappa@acme.de", "patient110", "76149"
            ),
            self._create_patient(
                120, "Lambda", "lambda@acme.de", "patient120", "76151"
            ),
            self._create_patient(
                130, "Mueller", "mueller@acme.de", "patient130", "76153"
            ),
            self._create_patient(
                140, "Neumann", "neumann@acme.de", "patient140", "76155"
            ),
            self._create_patient(
                150, "Schmidt", "schmidt@acme.de", "patient150", "76157"
            ),
            self._create_patient(160, "Weber", "weber@acme.de", "patient160", "76159"),
            self._create_patient(
                170, "Wagner", "wagner@acme.de", "patient170", "76161"
            ),
            self._create_patient(
                180, "Fischer", "fischer@acme.de", "patient180", "76163"
            ),
            self._create_patient(
                190, "Becker", "becker@acme.de", "patient190", "76165"
            ),
            self._create_patient(
                200, "Hoffmann", "hoffmann@acme.de", "patient200", "76167"
            ),
            self._create_patient(210, "Koch", "koch@acme.de", "patient210", "76169"),
        )

    def find_by_id(
        self,
        patient_id: int | None,
        session: Any = None,  # noqa: ARG002
    ) -> Patient | None:
        """Suche Patient anhand der ID."""
        if patient_id is None:
            return None

        return next(
            (patient for patient in self.patienten if patient.id == patient_id),
            None,
        )

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
        session: Any = None,  # noqa: ARG002
    ) -> Slice[Patient]:
        """Suche Patienten anhand von Query-Parametern."""
        patienten = list(self.patienten)

        if email := suchparameter.get("email"):
            patienten = [
                patient
                for patient in patienten
                if patient.email.lower() == email.lower()
            ]

        if nachname := suchparameter.get("nachname"):
            patienten = [
                patient
                for patient in patienten
                if nachname.lower() in patient.nachname.lower()
            ]

        total_elements = len(patienten)

        if pageable.size != 0:
            start = pageable.number * pageable.size
            ende = start + pageable.size
            patienten = patienten[start:ende]

        return Slice(content=tuple(patienten), total_elements=total_elements)

    def find_nachnamen(
        self,
        teil: str,
        session: Any = None,  # noqa: ARG002
    ) -> Sequence[str]:
        """Suche Nachnamen anhand eines Teilstrings."""
        teil_lower = teil.lower()

        return tuple(
            sorted(
                {
                    patient.nachname
                    for patient in self.patienten
                    if teil_lower in patient.nachname.lower()
                }
            )
        )

    def _create_patient(
        self,
        patient_id: int,
        nachname: str,
        email: str,
        username: str,
        plz: str,
    ) -> Patient:
        adresse = Adresse(
            id=patient_id,
            plz=plz,
            ort="Karlsruhe",
            patient_id=patient_id,
            patient=None,
        )

        patient = Patient(
            id=patient_id,
            version=0,
            nachname=nachname,
            email=email,
            kategorie=1,
            has_newsletter=True,
            geburtsdatum=date(2000, 1, 1),
            homepage="https://www.example.com",
            geschlecht=Geschlecht.MAENNLICH,
            familienstand=Familienstand.LEDIG,
            fachaerzte=[Facharzt.CHIRURGIE],
            username=username,
            adresse=adresse,
            rechnungen=[],
        )

        adresse.patient = patient

        return patient
