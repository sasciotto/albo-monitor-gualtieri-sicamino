from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from hashlib import sha256


@dataclass(slots=True)
class Act:
    """Rappresenta una pubblicazione dell'albo pretorio."""

    repertorio: str
    title: str
    typology: str = ""
    requester: str = ""
    start_date: date | None = None
    end_date: date | None = None
    detail_url: str = ""
    source_url: str = ""
    content_hash: str = ""

    @property
    def stable_id(self) -> str:
        """ID stabile usato per deduplica.

        Il repertorio è preferito quando disponibile. Se manca, viene creato un
        identificativo deterministico dai campi principali.
        """
        rep = normalize_text(self.repertorio)
        if rep:
            return rep

        raw = "|".join(
            [
                normalize_text(self.title),
                normalize_text(self.typology),
                self.start_date.isoformat() if self.start_date else "",
                self.detail_url,
            ]
        )
        return sha256(raw.encode("utf-8")).hexdigest()[:16]


def normalize_text(value: str | None) -> str:
    """Normalizza spazi e valori nulli."""
    return " ".join((value or "").split()).strip()
