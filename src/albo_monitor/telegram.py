from __future__ import annotations

import requests


TELEGRAM_LIMIT = 4096


class TelegramError(RuntimeError):
    """Errore durante l'invio Telegram."""


def split_message(text: str, limit: int = TELEGRAM_LIMIT) -> list[str]:
    """Divide il testo rispettando il limite Telegram."""
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for line in text.splitlines():
        line_len = len(line) + 1
        if current and current_len + line_len > limit:
            chunks.append("\n".join(current))
            current = []
            current_len = 0
        current.append(line)
        current_len += line_len

    if current:
        chunks.append("\n".join(current))
    return chunks


def send_message(token: str, chat_id: str, text: str) -> None:
    token = (token or "").strip()
    chat_id = (chat_id or "").strip()
    if not token:
        raise ValueError("Bot token Telegram mancante")
    if not chat_id:
        raise ValueError("Chat ID Telegram mancante")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    for chunk in split_message(text):
        try:
            response = requests.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": chunk,
                    "disable_web_page_preview": True,
                },
                timeout=25,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            detail = ""
            try:
                detail = f" - {response.text}"  # type: ignore[name-defined]
            except Exception:
                pass
            raise TelegramError(f"Invio Telegram non riuscito: {exc}{detail}") from exc
