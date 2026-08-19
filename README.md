# Albo Monitor

Monitor automatico per Albi Pretori online con struttura tabellare compatibile, con configurazione predefinita per il Comune di Gualtieri Sicaminò.

Il progetto legge le pubblicazioni dall'Albo Pretorio online, estrae i dati principali degli atti, filtra il periodo di interesse e invia un riepilogo tramite Telegram usando GitHub Actions.

> Progetto indipendente e non ufficiale. Non è affiliato ad alcun ente pubblico. Le informazioni devono essere sempre verificate sul sito istituzionale del Comune di riferimento.

## Uso per altri Comuni

Il progetto può essere riutilizzato anche per il proprio Comune di riferimento, purché l'Albo Pretorio online utilizzi una struttura compatibile con quella prevista dallo scraper.

La compatibilità è generalmente presente quando la pagina dell'albo espone una tabella HTML con campi simili a:

```text
repertorio / numero atto
titolo / oggetto
tipologia
richiedente / ufficio
inizio pubblicazione
fine pubblicazione
link di dettaglio
```

e quando la paginazione segue un parametro simile a:

```text
?page=1
?page=2
?page=3
```

Per usare un altro Comune è sufficiente impostare l'URL dell'albo tramite:

```env
ALBO_BASE_URL=https://esempio-comune.it/albo-pretorio
```

Se il sito utilizza una struttura diversa, ad esempio caricamento solo via JavaScript, colonne con ordine differente o paginazione non standard, potrebbe essere necessario adattare `src/albo_monitor/scraper.py`.

## Funzionalità

- Lettura paginata dell'Albo Pretorio online.
- Estrazione di repertorio, titolo, tipologia, richiedente, data inizio, data fine e link di dettaglio.
- Configurazione dell'URL dell'albo tramite variabile ambiente.
- Riepilogo Telegram con icone, statistiche per tipologia e lista degli atti rilevati.
- Filtro base per omettere dal riepilogo alcune pubblicazioni potenzialmente sensibili.
- Esecuzione automatica settimanale tramite GitHub Actions.
- Comandi locali per test, report Markdown e aggiornamento database SQLite.

## Architettura

```text
GitHub Actions
→ esecuzione pianificata
→ lettura dell'Albo Pretorio
→ filtro sugli ultimi giorni
→ generazione riepilogo
→ invio Telegram
```

Il workflow principale è disponibile in:

```text
.github/workflows/weekly-telegram.yml
```

## Requisiti

- Python 3.10 o superiore.
- Un Albo Pretorio online con struttura compatibile.
- Un bot Telegram creato tramite BotFather.
- L'ID destinatario Telegram, relativo a utente, gruppo o canale.
- Un repository GitHub con Actions abilitate.

## Installazione locale

Aprire PowerShell nella cartella del progetto:

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

Copiare `.env.example` in `.env` e impostare i valori richiesti:

```env
ALBO_BASE_URL=https://comune.gualtieri.me.it/albo-pretorio
ALBO_TELEGRAM_BOT_TOKEN=token_del_bot
ALBO_TELEGRAM_DESTINATION_ID=id_destinatario
```

Per un altro Comune, sostituire `ALBO_BASE_URL` con l'indirizzo dell'Albo Pretorio compatibile.

Il file `.env` contiene dati sensibili e non deve essere pubblicato.

## Comandi principali

Stampa del riepilogo senza invio:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main telegram-weekly --dry-run
```

Test su un altro Albo Pretorio compatibile:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main --base-url "https://esempio-comune.it/albo-pretorio" telegram-weekly --dry-run
```

Invio di un messaggio di prova:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main test-telegram
```

Invio del riepilogo settimanale:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main telegram-weekly
```

Aggiornamento database SQLite locale:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main fetch --max-pages 5
```

Generazione report Markdown dal database locale:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main report
```

## GitHub Actions

Nel repository configurare i repository secrets:

```text
ALBO_TELEGRAM_BOT_TOKEN
ALBO_TELEGRAM_DESTINATION_ID
```

Per usare un Comune diverso da quello predefinito, configurare anche una repository variable:

```text
ALBO_BASE_URL
```

Percorsi:

```text
Settings → Secrets and variables → Actions → Secrets
Settings → Secrets and variables → Actions → Variables
```

Avvio manuale:

```text
Actions → Weekly Telegram report → Run workflow
```

## Privacy e limiti

Il progetto elabora dati pubblicati su un albo online, ma la disponibilità pubblica non implica che ogni informazione debba essere conservata o ridistribuita senza criterio.

Per questo motivo il riepilogo applica un filtro base su alcune parole chiave potenzialmente sensibili. Il filtro non sostituisce una valutazione giuridica, organizzativa o redazionale.

Il sistema non sostituisce la consultazione dell'Albo Pretorio ufficiale. In caso di dubbio, fare sempre riferimento alla fonte istituzionale del Comune di riferimento.

## Documentazione

Guida dettagliata:

```text
docs/INSTALLAZIONE.md
```

Indicazioni di sicurezza:

```text
SECURITY.md
```

## Licenza

MIT License.
