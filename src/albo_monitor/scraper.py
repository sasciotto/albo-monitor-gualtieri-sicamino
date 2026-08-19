from __future__ import annotations

from datetime import date, datetime
from hashlib import sha256
from typing import Iterable
from urllib.parse import urlencode, urljoin, urlparse, parse_qsl, urlunparse

import requests
from bs4 import BeautifulSoup

from .models import Act, normalize_text


class ScraperError(RuntimeError):
    """Errore durante la lettura dell'albo."""


def page_url(base_url: str, page: int) -> str:
    """Costruisce l'URL paginato mantenendo eventuali query string esistenti."""
    parsed = urlparse(base_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["page"] = str(page)
    return urlunparse(parsed._replace(query=urlencode(query)))


def fetch_html(url: str, timeout: int = 25) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; AlboMonitor/1.0; "
            "+https://github.com/)"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ScraperError(f"Impossibile leggere {url}: {exc}") from exc
    return response.text


def parse_date(value: str | None) -> date | None:
    text = normalize_text(value)
    if not text or text in {"-", "--"}:
        return None

    # Alcune pagine possono includere ora o testo aggiuntivo: teniamo il primo token.
    token = text.split()[0]
    formats = ["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d.%m.%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(token, fmt).date()
        except ValueError:
            continue
    return None


def parse_listing_html(html: str, source_url: str) -> list[Act]:
    """Estrae gli atti dalla pagina HTML dell'albo."""
    soup = BeautifulSoup(html, "html.parser")
    acts: list[Act] = []

    rows = soup.select("table tbody tr") or soup.select("table tr")
    for row in rows:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue

        texts = [normalize_text(cell.get_text(" ", strip=True)) for cell in cells]
        texts = [text for text in texts if text]
        if len(texts) < 3:
            continue

        # Salta eventuali intestazioni.
        first = texts[0].lower()
        if first in {"repertorio", "n.", "numero", "num"}:
            continue

        link_tag = row.find("a", href=True)
        detail_url = urljoin(source_url, link_tag["href"]) if link_tag else ""

        repertorio = texts[0] if len(texts) > 0 else ""
        title = texts[1] if len(texts) > 1 else ""
        typology = texts[2] if len(texts) > 2 else ""
        requester = texts[3] if len(texts) > 3 else ""
        start_date = parse_date(texts[4]) if len(texts) > 4 else None
        end_date = parse_date(texts[5]) if len(texts) > 5 else None

        raw = "|".join(texts + [detail_url])
        acts.append(
            Act(
                repertorio=repertorio,
                title=title,
                typology=typology,
                requester=requester,
                start_date=start_date,
                end_date=end_date,
                detail_url=detail_url,
                source_url=source_url,
                content_hash=sha256(raw.encode("utf-8")).hexdigest(),
            )
        )

    return acts


def scrape_pages(base_url: str, max_pages: int = 5) -> list[Act]:
    """Scarica più pagine dell'albo e restituisce atti deduplicati."""
    found: dict[str, Act] = {}

    for page in range(1, max_pages + 1):
        current_url = page_url(base_url, page)
        html = fetch_html(current_url)
        page_acts = parse_listing_html(html, current_url)
        if not page_acts:
            break

        before = len(found)
        for act in page_acts:
            found.setdefault(act.stable_id, act)

        # Se una pagina non introduce nulla di nuovo, probabilmente siamo oltre.
        if len(found) == before and page > 1:
            break

    return list(found.values())


def filter_since(acts: Iterable[Act], since: date) -> list[Act]:
    """Tiene gli atti con data inizio dal giorno indicato in poi.

    Se la data non è disponibile, l'atto viene mantenuto: è meglio segnalarlo
    che perderlo silenziosamente.
    """
    result = [act for act in acts if act.start_date is None or act.start_date >= since]
    return sorted(result, key=lambda act: (act.start_date or date.min, act.repertorio), reverse=True)
