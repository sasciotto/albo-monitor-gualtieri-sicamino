# Riassunto della chat

## Obiettivo iniziale

L'obiettivo era creare un sistema che producesse un resoconto settimanale delle pubblicazioni effettuate sull'Albo Pretorio del Comune di Gualtieri Sicaminò.

## Prima fase: monitor locale

È stato creato un primo progetto Python capace di:

- leggere la pagina dell'Albo Pretorio;
- estrarre le pubblicazioni;
- salvarle in un database SQLite;
- generare un report Markdown.

Il progetto è stato avviato su Windows tramite PowerShell. Dopo l'installazione di Python e la creazione dell'ambiente virtuale, il comando `fetch` ha letto correttamente 25 atti.

## Seconda fase: Telegram

È stata aggiunta la possibilità di inviare il riepilogo tramite Telegram.

Sono stati configurati:

- un bot Telegram creato con BotFather;
- il token del bot;
- il chat id personale;
- il comando `telegram-weekly`.

Dopo alcuni tentativi iniziali, il messaggio Telegram è arrivato correttamente.

## Terza fase: GitHub Actions

Il progetto è stato caricato su GitHub e configurato con un workflow automatico.

Sono stati risolti alcuni problemi:

- workflow YAML non valido;
- mancanza dei file `src` e `requirements.txt` nel repository;
- assenza dei GitHub Actions Secrets;
- token Telegram mancante nel workflow.

Alla fine il workflow GitHub Actions è diventato operativo e ha inviato il riepilogo Telegram fuori dal PC locale.

## Quarta fase: gruppo Telegram

Il bot inizialmente inviava il report solo alla chat privata. È stato poi recuperato il chat id del gruppo Telegram:

```text
-5542065339
```

È stato chiarito che il segno meno è necessario per i gruppi Telegram. Sostituendo il secret `ALBO_TELEGRAM_CHAT_ID` con l'id del gruppo, il report può essere ricevuto da tutti i membri del gruppo.

## Stato finale

Il sistema attuale:

- funziona da settimane;
- gira tramite GitHub Actions;
- invia il report su Telegram;
- può inviare il report anche a un gruppo;
- è pronto per essere ripulito e pubblicato come progetto GitHub pubblico.

## Decisione finale

La strategia consigliata è pubblicare una versione pulita del progetto, senza:

- token;
- chat id personali;
- database SQLite;
- log;
- ambiente virtuale;
- file `.env`.

Il progetto pubblico deve contenere solo codice, guida, licenza, workflow e file di esempio.
