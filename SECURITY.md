# Security

Non pubblicare token Telegram, chat id personali, file `.env`, database locali o log.

Se un token Telegram viene esposto accidentalmente:

1. apri BotFather;
2. seleziona il bot;
3. rigenera/revoca il token;
4. aggiorna il secret `ALBO_TELEGRAM_BOT_TOKEN` su GitHub.

I secrets devono essere configurati in GitHub Actions e non inseriti nei file del progetto.
