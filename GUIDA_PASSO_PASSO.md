# Guida passo passo

Questa guida spiega come usare e pubblicare il progetto partendo da zero.

## 1. Creare il bot Telegram

1. Apri Telegram.
2. Cerca `BotFather`.
3. Scrivi `/newbot`.
4. Scegli un nome, per esempio `Albo Gualtieri Monitor`.
5. Scegli uno username che finisca con `bot`.
6. Copia il token generato.

Il token è una password: non inserirlo nel codice e non pubblicarlo su GitHub.

## 2. Recuperare il chat id

Scrivi un messaggio al bot oppure aggiungi il bot a un gruppo e scrivi un messaggio nel gruppo.

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

Per una chat privata vedrai un id positivo. Per un gruppo vedrai un id negativo. Per esempio:

```text
-5542065339
```

Il segno meno è parte del valore e va mantenuto.

## 3. Provare in locale

Apri PowerShell nella cartella del progetto.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se l'attivazione viene bloccata:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Crea il file `.env` copiando `.env.example` e inserendo:

```env
ALBO_TELEGRAM_BOT_TOKEN=TOKEN_DEL_BOT
ALBO_TELEGRAM_CHAT_ID=CHAT_ID
```

Prova senza inviare:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main telegram-weekly --dry-run
```

Prova l'invio:

```powershell
$env:PYTHONPATH="src"
python -m albo_monitor.main telegram-weekly
```

## 4. Pubblicare su GitHub

Crea un repository GitHub, meglio se inizialmente privato.

Carica questi file e cartelle:

```text
.github/
src/
scripts/
tests/
examples/
README.md
GUIDA_PASSO_PASSO.md
RIASSUNTO_CHAT.md
requirements.txt
pyproject.toml
.env.example
.gitignore
LICENSE
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

## 5. Inserire i secrets su GitHub

Vai in:

```text
Settings → Secrets and variables → Actions → New repository secret
```

Aggiungi:

```text
ALBO_TELEGRAM_BOT_TOKEN
ALBO_TELEGRAM_CHAT_ID
```

## 6. Testare GitHub Actions

Vai in:

```text
Actions → Weekly Telegram report → Run workflow
```

Se il run diventa verde e arriva il messaggio nel gruppo Telegram, il servizio è pronto.

## 7. Rendere pubblico il repository

Prima di impostare il repository come pubblico:

- verifica che non ci siano token;
- verifica che non ci siano database;
- verifica che non ci siano log;
- verifica che `.env` non sia presente;
- verifica che il README dica che il progetto non è ufficiale.

Poi vai in:

```text
Settings → General → Danger Zone → Change repository visibility
```

Scegli `Public`.
