# Albo Monitor - Gualtieri Sicaminò

Monitor automatico dell'Albo Pretorio del Comune di Gualtieri Sicaminò.

Il progetto legge le pubblicazioni dall'albo pretorio online, filtra gli atti recenti e invia un riepilogo Telegram tramite GitHub Actions.

> Progetto indipendente e non ufficiale. Non è affiliato al Comune di Gualtieri Sicaminò.

## Funzionalità

- Lettura dell'Albo Pretorio online.
- Estrazione di repertorio, titolo, tipologia, richiedente, data inizio, data fine e link.
- Report Telegram con simboli, riepilogo per tipologia e lista pubblicazioni.
- Filtro base per omettere atti potenzialmente sensibili.
- Automazione settimanale con GitHub Actions.
- Comandi locali per test, report Markdown e invio Telegram.

## Come funziona

```text
GitHub Actions
→ avvia lo script ogni lunedì
→ scarica l'albo pretorio
→ filtra gli atti degli ultimi 7 giorni
→ genera il messaggio
→ invia il riepilogo su Telegram
```

GitHub Actions supporta workflow avviabili manualmente con `workflow_dispatch` e pianificabili con `schedule` usando cron POSIX. I valori sensibili, come il token Telegram, devono essere salvati nei repository secrets e richiamati nel workflow, non scritti nel codice.

## Requisiti locali

- Python 3.10 o superiore.
- Un bot Telegram creato con BotFather.
- Un chat id Telegram personale, di gruppo o di canale.

## Installazione locale su Windows

Apri PowerShell nella cartella del progetto e lancia:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se PowerShell blocca l'attivazione dell'ambiente virtuale:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Configurazione locale

Copia `.env.example` in `.env` e inserisci i tuoi valori:

```env
ALBO_TELEGRAM_BOT_TOKEN=token_del_bot
ALBO_TELEGRAM_CHAT_ID=id_chat_o_gruppo
```

Non pubblicare mai `.env`.

## Test locale

Stampa il report senza inviarlo:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main telegram-weekly --dry-run
```

Invia un messaggio di prova:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main test-telegram
```

Invia il report vero:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main telegram-weekly
```

Aggiorna un database locale SQLite:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main fetch --max-pages 5
```

Genera un report Markdown dal database locale:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main report
```

## Configurazione GitHub Actions

Nel repository GitHub vai in:

```text
Settings → Secrets and variables → Actions → New repository secret
```

Crea questi due secrets:

```text
ALBO_TELEGRAM_BOT_TOKEN
ALBO_TELEGRAM_CHAT_ID
```

Per un gruppo Telegram, il chat id è di solito negativo, ad esempio:

```text
-5542065339
```

Il segno meno va mantenuto.

Il workflow principale si trova in:

```text
.github/workflows/weekly-telegram.yml
```

Puoi provarlo da:

```text
Actions → Weekly Telegram report → Run workflow
```

## Pubblicazione del repository

Prima di rendere pubblico il progetto, verifica che non siano presenti:

```text
.venv/
.env
data/
logs/
reports/
*.sqlite
*.db
token Telegram
chat id personali
```

Il file `.gitignore` incluso esclude già questi elementi.

## Privacy

Il progetto usa dati presenti su un albo pubblico, ma non significa che sia opportuno conservare o ridiffondere tutto senza criterio. Per questo il report Telegram omette alcune tipologie potenzialmente sensibili tramite parole chiave base.

Il sistema non sostituisce la consultazione dell'albo ufficiale. Per ogni atto è sempre opportuno verificare il sito istituzionale.

## Licenza

MIT License.
