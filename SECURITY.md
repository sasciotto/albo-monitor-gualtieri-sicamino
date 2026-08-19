# Sicurezza

Il progetto richiede un token Telegram per l'invio dei messaggi. Il token deve essere gestito come dato sensibile.

## Regole operative

- Non inserire token o identificativi reali nei file del repository.
- Usare i repository secrets di GitHub Actions per `ALBO_TELEGRAM_BOT_TOKEN` e `ALBO_TELEGRAM_DESTINATION_ID`.
- Usare una repository variable per `ALBO_BASE_URL` quando si monitora un Comune diverso da quello predefinito.
- Non pubblicare `.env`, database SQLite, log, report o cartelle locali.
- In caso di esposizione accidentale del token, revocarlo e generarne uno nuovo tramite BotFather.

## Dati trattati

Il progetto elabora informazioni pubblicate su un Albo Pretorio online. La disponibilità pubblica della fonte non elimina la necessità di valutare con attenzione conservazione, ridistribuzione e contenuto dei riepiloghi.
