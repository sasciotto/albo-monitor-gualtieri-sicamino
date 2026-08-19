from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path

from . import config
from .report import redact_sensitive, render_markdown, render_telegram
from .scraper import filter_since, scrape_pages
from .storage import list_since, upsert_acts
from .telegram import send_message


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="albo-monitor")
    parser.add_argument("--db", default=config.db_path(), help="Percorso database SQLite")
    parser.add_argument("--base-url", default=config.base_url(), help="URL base albo pretorio")

    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="Scarica l'albo e aggiorna il database locale")
    fetch.add_argument("--max-pages", type=int, default=config.max_pages())

    report = sub.add_parser("report", help="Genera report Markdown dal database locale")
    report.add_argument("--days", type=int, default=config.DEFAULT_DAYS)
    report.add_argument("--output", default="reports/weekly.md")
    report.add_argument("--include-sensitive", action="store_true")

    weekly = sub.add_parser("telegram-weekly", help="Scarica gli atti recenti e invia il report Telegram")
    weekly.add_argument("--days", type=int, default=config.DEFAULT_DAYS)
    weekly.add_argument("--max-pages", type=int, default=config.max_pages())
    weekly.add_argument("--source", choices=["live", "db"], default="live")
    weekly.add_argument("--dry-run", action="store_true", help="Stampa il messaggio senza inviare")
    weekly.add_argument("--include-sensitive", action="store_true")

    test = sub.add_parser("test-telegram", help="Invia un messaggio Telegram di prova")
    test.add_argument("--text", default="✅ Test Albo Monitor: invio Telegram funzionante.")

    return parser


def since_from_days(days: int) -> date:
    if days < 1:
        raise ValueError("--days deve essere almeno 1")
    return date.today() - timedelta(days=days)


def cmd_fetch(args: argparse.Namespace) -> int:
    acts = scrape_pages(args.base_url, args.max_pages)
    new_count, updated_count = upsert_acts(args.db, acts)
    print(f"Letti {len(acts)} atti. Nuovi: {new_count}. Aggiornati: {updated_count}.")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    since = since_from_days(args.days)
    acts = list_since(args.db, since)
    acts, redacted = redact_sensitive(acts, enabled=not args.include_sensitive)
    text = render_markdown(acts, since, redacted)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(f"Report generato: {output}")
    return 0


def _weekly_acts(args: argparse.Namespace, since: date):
    if args.source == "db":
        return list_since(args.db, since)
    acts = scrape_pages(args.base_url, args.max_pages)
    return filter_since(acts, since)


def cmd_telegram_weekly(args: argparse.Namespace) -> int:
    since = since_from_days(args.days)
    acts = _weekly_acts(args, since)
    acts, redacted = redact_sensitive(acts, enabled=not args.include_sensitive)
    text = render_telegram(acts, since, redacted)

    if args.dry_run:
        print(text)
        return 0

    send_message(config.telegram_token(), config.telegram_chat_id(), text)
    print("Report Telegram inviato.")
    return 0


def cmd_test_telegram(args: argparse.Namespace) -> int:
    send_message(config.telegram_token(), config.telegram_chat_id(), args.text)
    print("Messaggio Telegram di prova inviato.")
    return 0


def main() -> None:
    config.load_dotenv()
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "fetch": cmd_fetch,
        "report": cmd_report,
        "telegram-weekly": cmd_telegram_weekly,
        "test-telegram": cmd_test_telegram,
    }
    raise SystemExit(commands[args.command](args))


if __name__ == "__main__":
    main()
