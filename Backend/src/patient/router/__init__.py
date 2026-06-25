# Copyright (C) 2023 - present Juergen Zimmermann, Hochschule Karlsruhe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Modul für die REST-Schnittstelle einschließlich Validierung."""

from collections.abc import Sequence

from patient.router.health_router import liveness, readiness
from patient.router.health_router import router as health_router
from patient.router.patient_router import get, get_by_id, get_nachnamen, patient_router

__all__: Sequence[str] = [
    "get",
    "get_by_id",
    "get_nachnamen",
    "health_router",
    "liveness",
    "patient_router",
    "readiness",
]
