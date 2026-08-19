from __future__ import annotations

from collections import Counter
from datetime import date

from .models import Act, normalize_text


SENSITIVE_KEYWORDS = [
    "matrimonio",
    "pubblicazione di matrimonio",
    "nascita",
    "adozione",
    "minore",
    "residenza",
    "irreperibilità",
    "notifica",
    "notifiche",
    "anagrafe",
    "stato civile",
]


def is_sensitive(act: Act) -> bool:
    haystack = " ".join([act.title, act.typology, act.requester]).lower()
    return any(keyword in haystack for keyword in SENSITIVE_KEYWORDS)


def redact_sensitive(acts: list[Act], enabled: bool = True) -> tuple[list[Act], int]:
    if not enabled:
        return acts, 0
    safe = [act for act in acts if not is_sensitive(act)]
    return safe, len(acts) - len(safe)


def typology_icon(typology: str) -> str:
    text = typology.lower()
    if "determina" in text:
        return "📝"
    if "delib" in text:
        return "🏛"
    if "ordinanza" in text:
        return "⚠️"
    if "avviso" in text:
        return "📢"
    if "bando" in text or "gara" in text:
        return "📑"
    if "matrimonio" in text:
        return "🔒"
    return "📄"


def shorten(text: str, max_len: int = 220) -> str:
    clean = normalize_text(text)
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 1].rstrip() + "…"


def render_telegram(acts: list[Act], since: date, redacted: int = 0, max_items: int = 40) -> str:
    """Crea il testo del messaggio Telegram.

    Non usa Markdown/HTML parse mode, così riduce il rischio di errori dovuti
    a caratteri speciali negli atti.
    """
    by_type = Counter(act.typology or "Senza tipologia" for act in acts)

    lines = [
        "📋 Albo Pretorio - Gualtieri Sicaminò",
        f"📅 Periodo: dal {since.isoformat()} a oggi",
        f"📌 Pubblicazioni rilevate: {len(acts)}",
    ]

    if redacted:
        lines.append(f"🔒 Atti potenzialmente sensibili omessi: {redacted}")

    if by_type:
        lines.extend(["", "📊 Riepilogo per tipologia:"])
        for typology, count in by_type.most_common():
            lines.append(f"• {typology_icon(typology)} {typology}: {count}")

    lines.extend(["", "🗂 Pubblicazioni:"])

    if not acts:
        lines.append("✅ Nessuna nuova pubblicazione rilevata nel periodo.")
        return "\n".join(lines)

    visible = acts[:max_items]
    for index, act in enumerate(visible, start=1):
        start = act.start_date.isoformat() if act.start_date else "-"
        end = act.end_date.isoformat() if act.end_date else "-"
        typology = act.typology or "Senza tipologia"

        lines.extend(
            [
                "",
                f"🔹 {index}. Repertorio: {act.repertorio or '-'}",
                f"   📅 Inizio/Fine: {start} → {end}",
                f"   🏷 Tipologia: {typology}",
                f"   📄 Titolo: {shorten(act.title)}",
            ]
        )
        if act.detail_url:
            lines.append(f"   🔗 Link: {act.detail_url}")

    remaining = len(acts) - len(visible)
    if remaining > 0:
        lines.extend(["", f"… altri {remaining} atti non mostrati per brevità."])

    return "\n".join(lines)


def render_markdown(acts: list[Act], since: date, redacted: int = 0) -> str:
    by_type = Counter(act.typology or "Senza tipologia" for act in acts)
    lines = [
        "# Report Albo Pretorio - Gualtieri Sicaminò",
        "",
        f"**Periodo:** dal {since.isoformat()} a oggi",
        f"**Pubblicazioni rilevate:** {len(acts)}",
    ]
    if redacted:
        lines.append(f"**Atti potenzialmente sensibili omessi:** {redacted}")

    lines.extend(["", "## Riepilogo per tipologia", ""])
    if by_type:
        for typology, count in by_type.most_common():
            lines.append(f"- {typology}: {count}")
    else:
        lines.append("- Nessuna pubblicazione rilevata")

    lines.extend(["", "## Pubblicazioni", ""])
    for act in acts:
        start = act.start_date.isoformat() if act.start_date else "-"
        end = act.end_date.isoformat() if act.end_date else "-"
        lines.extend(
            [
                f"### {act.repertorio or '-'}",
                "",
                f"- **Titolo:** {act.title}",
                f"- **Tipologia:** {act.typology or '-'}",
                f"- **Inizio:** {start}",
                f"- **Fine:** {end}",
            ]
        )
        if act.detail_url:
            lines.append(f"- **Link:** {act.detail_url}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
