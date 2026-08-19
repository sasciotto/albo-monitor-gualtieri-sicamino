# Installazione e configurazione

Questa guida descrive la configurazione completa del progetto, dall'esecuzione locale all'automazione con GitHub Actions.

## 1. Compatibilità dell'Albo Pretorio

Il progetto è configurato in modo predefinito per l'Albo Pretorio del Comune di Gualtieri Sicaminò, ma può essere utilizzato anche per altri Comuni.

Il riuso è possibile quando l'Albo Pretorio del Comune di riferimento usa una struttura compatibile, cioè una pagina con tabella HTML e campi simili a:

```text
repertorio / numero atto
titolo / oggetto
tipologia
richiedente / ufficio
inizio pubblicazione
fine pubblicazione
link di dettaglio
```

La paginazione deve essere compatibile con un parametro numerico, ad esempio:

```text
https://esempio-comune.it/albo-pretorio?page=1
https://esempio-comune.it/albo-pretorio?page=2
```

Per verificare un Comune diverso, eseguire un test locale sostituendo l'URL:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main --base-url "https://esempio-comune.it/albo-pretorio" telegram-weekly --dry-run
```

Se il risultato mostra gli atti nel formato corretto, la struttura è compatibile. Se non vengono trovati atti o i campi risultano disordinati, è necessario adattare lo scraper.

## 2. Preparare il bot Telegram

1. Aprire Telegram.
2. Cercare `BotFather`.
3. Eseguire il comando `/newbot`.
4. Scegliere un nome descrittivo per il bot.
5. Scegliere uno username che termini con `bot`.
6. Conservare il token fornito da BotFather.

Il token del bot è un dato sensibile e deve essere trattato come una password.

## 3. Recuperare l'ID destinatario Telegram

Inviare almeno un messaggio al bot, oppure aggiungere il bot a un gruppo e inviare un messaggio nel gruppo.

Da PowerShell:

```powershell
$token="TOKEN_DEL_BOT"
$r = Invoke-RestMethod "https://api.telegram.org/bot$token/getUpdates"
$r.result | ForEach-Object {
    if ($_.message) { $_.message.chat }
    elseif ($_.my_chat_member) { $_.my_chat_member.chat }
    elseif ($_.chat_member) { $_.chat_member.chat }
}
```

Nel risultato individuare il campo `id` relativo al destinatario scelto.

Per gruppi e canali il valore può essere negativo. Il segno meno è parte dell'identificativo e deve essere mantenuto.

## 4. Installazione locale su Windows

Aprire PowerShell nella cartella del progetto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se l'attivazione dell'ambiente virtuale viene bloccata:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 5. Configurazione locale

Creare un file `.env` partendo da `.env.example`:

```env
ALBO_BASE_URL=https://comune.gualtieri.me.it/albo-pretorio
ALBO_MAX_PAGES=5
ALBO_DB=data/albo.sqlite

ALBO_TELEGRAM_BOT_TOKEN=TOKEN_DEL_BOT
ALBO_TELEGRAM_DESTINATION_ID=ID_DESTINATARIO
```

Per un Comune diverso, sostituire `ALBO_BASE_URL` con l'indirizzo del relativo Albo Pretorio compatibile.

Il file `.env` non deve essere pubblicato.

## 6. Verifica locale

Eseguire una prova senza inviare messaggi:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main telegram-weekly --dry-run
```

Eseguire una prova su un URL diverso:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main --base-url "https://esempio-comune.it/albo-pretorio" telegram-weekly --dry-run
```

Eseguire un messaggio di prova:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main test-telegram
```

Inviare il riepilogo:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main telegram-weekly
```

## 7. Pubblicazione su GitHub

Caricare nel repository solo i file necessari:

```text
.github/
docs/
examples/
scripts/
src/
tests/
.env.example
.gitignore
LICENSE
README.md
SECURITY.md
pyproject.toml
requirements.txt
```

Non caricare:

```text
.venv/
.env
data/
logs/
reports/
*.sqlite
*.db
```

## 8. Configurazione dei secrets GitHub

Nel repository aprire:

```text
Settings → Secrets and variables → Actions → Secrets → New repository secret
```

Creare i seguenti secrets:

```text
ALBO_TELEGRAM_BOT_TOKEN
ALBO_TELEGRAM_DESTINATION_ID
```

I valori reali devono essere inseriti solo nei secrets, non nei file del repository.

## 9. Configurazione opzionale per un altro Comune

Se il progetto deve monitorare un Comune diverso da quello predefinito, aprire:

```text
Settings → Secrets and variables → Actions → Variables → New repository variable
```

Creare la variabile:

```text
ALBO_BASE_URL
```

con valore simile a:

```text
https://esempio-comune.it/albo-pretorio
```

La variabile deve puntare alla pagina principale dell'Albo Pretorio compatibile, senza il parametro `page`, salvo casi specifici.

## 10. Avvio manuale del workflow

Aprire:

```text
Actions → Weekly Telegram report → Run workflow
```

Se il run termina correttamente e il messaggio viene ricevuto su Telegram, la configurazione è operativa.

## 11. Pianificazione

Il workflow incluso usa una pianificazione settimanale:

```yaml
schedule:
  - cron: "17 6 * * 1"
```

L'orario è espresso in UTC. In Italia corrisponde indicativamente alle 07:17 o 08:17, a seconda dell'ora solare o legale.

## 12. Storico opzionale

Il file seguente contiene un esempio opzionale per salvare uno storico SQLite nel repository:

```text
examples/workflows/daily-history.yml
```

In un repository pubblico è preferibile non pubblicare database o storici, perché potrebbero contenere dati personali presenti negli atti.
