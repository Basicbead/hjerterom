#!/bin/zsh
set -e
cd "$(dirname "$0")"

if command -v ollama >/dev/null 2>&1; then
  OLLAMA_BIN="$(command -v ollama)"
elif [[ -x "/Applications/Ollama.app/Contents/Resources/ollama" ]]; then
  OLLAMA_BIN="/Applications/Ollama.app/Contents/Resources/ollama"
else
  echo "Installerer Ollama fra den offisielle installasjonskilden …"
  if ! command -v curl >/dev/null 2>&1; then
    echo "Fant ikke curl. Installer Ollama fra https://ollama.com/download/mac og kjør fila på nytt."
    read "?Trykk Enter for å avslutte. "
    exit 1
  fi
  curl -fsSL https://ollama.com/install.sh | sh
  if command -v ollama >/dev/null 2>&1; then
    OLLAMA_BIN="$(command -v ollama)"
  elif [[ -x "/Applications/Ollama.app/Contents/Resources/ollama" ]]; then
    OLLAMA_BIN="/Applications/Ollama.app/Contents/Resources/ollama"
  else
    echo "Ollama-installasjonen ble ikke funnet etter installasjonen."
    echo "Installer Ollama fra https://ollama.com/download/mac og kjør fila på nytt."
    read "?Trykk Enter for å avslutte. "
    exit 1
  fi
fi

if ! curl -fsS --max-time 2 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  ("$OLLAMA_BIN" serve >/tmp/hjerterom-ollama.log 2>&1 &)
  for i in {1..20}; do
    if curl -fsS --max-time 2 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then break; fi
    sleep 1
  done
fi

if ! curl -fsS --max-time 2 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  echo "Klarte ikke å starte Ollama. Åpne Ollama fra Programmer og prøv igjen."
  read "?Trykk Enter for å avslutte. "
  exit 1
fi

if ! "$OLLAMA_BIN" list | awk 'NR>1 {print $1}' | grep -qx 'gemma3:1b'; then
  echo "Laster ned Gemma (ca. 806 MB). Dette trengs bare første gang."
  "$OLLAMA_BIN" pull gemma3:1b
fi

if ! "$OLLAMA_BIN" list | awk 'NR>1 {print $1}' | grep -qx 'hjerterom:latest'; then
  echo "Klargjør Hjerterom med egne regler for trygge og respektfulle råd …"
  "$OLLAMA_BIN" create hjerterom -f Modelfile
fi

if ! curl -fsS --max-time 2 http://127.0.0.1:8765/api/status >/dev/null 2>&1; then
  python3 server.py &
  server_pid=$!
  trap 'kill "$server_pid" 2>/dev/null || true' EXIT
  sleep 1
  open http://127.0.0.1:8765
  wait "$server_pid"
else
  open http://127.0.0.1:8765
  echo "Hjerterom er allerede startet i nettleseren."
  read "?Trykk Enter for å avslutte. "
fi
