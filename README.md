# Hjerterom

En lokal samtaleassistent for kjærlighets- og relasjonsråd på Mac. Den bruker Gemma 3 1B gjennom Ollama. Samtaler går til Ollama på samme maskin og lagres ikke av appen.

## Kom i gang

1. Installer [Ollama for Mac](https://ollama.com/download/mac) (macOS 14 eller nyere).
2. Pakk ut nedlastingen.
3. Dobbeltklikk `START-ME.command` og velg **Åpne** hvis macOS spør.
4. Første gang laster Ollama automatisk ned Gemma-modellen (omtrent 806 MB). La Terminal-vinduet stå åpent mens du bruker Hjerterom.

Etter første oppsett kan Hjerterom brukes uten internett. Start det senere med `START-ME.command`.

## Innhold

- `index.html` – chat-grensesnittet
- `server.py` – lokal server som bare lytter på denne Mac-en
- `Modelfile` – Gemma-modell med instruksjoner for kjærlighetsråd
- `START-ME.command` – starter Ollama, klargjør Gemma og åpner Hjerterom
- `LES-MEG.txt` – norsk bruksanvisning

Assistenten kan ta feil og erstatter ikke profesjonell hjelp. Ikke del informasjon du ikke ønsker å skrive til en lokal språkmodell.
