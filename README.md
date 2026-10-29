# Hjerterom

En lokal samtaleassistent for kjærlighets- og relasjonsråd på Mac. Den bruker Gemma 3 1B gjennom Ollama. Samtalene behandles lokalt og lagres ikke av appen.

## Én nedlasting, enkelt oppsett

1. Last ned ZIP-filen fra **Assets** i [siste release](https://github.com/Basicbead/hjerterom/releases/latest).
2. Pakk ut ZIP-filen og dobbeltklikk `START-ME.command`.
3. Hvis Ollama mangler, starter fila den offisielle installasjonen. Første gang lastes Gemma-modellen også ned (omtrent 806 MB).
4. La Terminal-vinduet stå åpent mens du bruker Hjerterom.

Du trenger internett under førstegangsoppsettet. Etterpå kjører Hjerterom lokalt og kan brukes uten internett. macOS 14 eller nyere kreves.

## Innhold

- `index.html` – chat-grensesnittet
- `server.py` – lokal server som bare lytter på denne Mac-en
- `Modelfile` – Gemma-modell med instruksjoner for kjærlighetsråd
- `START-ME.command` – installerer Ollama om nødvendig, klargjør Gemma og åpner Hjerterom
- `LES-MEG.txt` – norsk bruksanvisning

Assistenten kan ta feil og erstatter ikke profesjonell hjelp. Ikke del informasjon du ikke ønsker å skrive til en lokal språkmodell.
