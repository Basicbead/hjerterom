#!/usr/bin/env python3
"""Loopback-only chat UI proxy for a local Ollama model. No chats are stored."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8765
MODEL = "hjerterom"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


class Handler(BaseHTTPRequestHandler):
    server_version = "HjerteromLocal/1.0"

    def log_message(self, fmt, *args):
        # Avoid recording message content or chat history in terminal logs.
        if self.path != "/api/chat":
            super().log_message(fmt, *args)

    def _send(self, status, payload, content_type="application/json; charset=utf-8"):
        data = payload if isinstance(payload, bytes) else payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, (ROOT / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/status":
            try:
                req = urllib.request.Request("http://127.0.0.1:11434/api/tags", method="GET")
                with urllib.request.urlopen(req, timeout=2) as response:
                    data = json.loads(response.read().decode("utf-8"))
                ready = any(m.get("name", "").split(":")[0] == MODEL for m in data.get("models", []))
                self._send(200, json.dumps({"ready": ready, "model": MODEL}))
            except Exception:
                self._send(200, json.dumps({"ready": False, "model": MODEL, "engine": False}))
        else:
            self._send(404, json.dumps({"error": "Fant ikke siden."}))

    def do_POST(self):
        if self.path != "/api/chat":
            self._send(404, json.dumps({"error": "Fant ikke endepunktet."}))
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 1 or size > 48_000:
                self._send(413, json.dumps({"error": "Meldingen er for stor."}))
                return
            incoming = json.loads(self.rfile.read(size).decode("utf-8"))
            messages = incoming.get("messages", [])
            if not isinstance(messages, list) or not messages or len(messages) > 16:
                self._send(400, json.dumps({"error": "Samtalen har ugyldig format."}))
                return
            clean = []
            for msg in messages:
                role = msg.get("role")
                content = msg.get("content")
                if role not in ("user", "assistant") or not isinstance(content, str):
                    continue
                clean.append({"role": role, "content": content[:4000]})
            if not clean or clean[-1]["role"] != "user":
                self._send(400, json.dumps({"error": "Skriv et spørsmål først."}))
                return
            body = json.dumps({
                "model": MODEL,
                "messages": clean,
                "stream": False,
                "options": {"num_ctx": 2048, "num_predict": 420},
            }).encode("utf-8")
            req = urllib.request.Request(OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as response:
                result = json.loads(response.read().decode("utf-8"))
            answer = result.get("message", {}).get("content", "").strip()
            if not answer:
                raise ValueError("Modellen returnerte ikke et svar.")
            self._send(200, json.dumps({"answer": answer}, ensure_ascii=False))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:500]
            if exc.code == 404:
                message = "Modellen er ikke klargjort ennå. Kjør START-ME.command på nytt med internett til modellnedlastingen er ferdig."
            else:
                message = "Den lokale AI-motoren svarte med en feil. Start Ollama på nytt og prøv igjen."
            self._send(503, json.dumps({"error": message, "detail": detail}, ensure_ascii=False))
        except (OSError, TimeoutError):
            self._send(503, json.dumps({"error": "Finner ikke den lokale AI-motoren. Kontroller at Ollama kjører."}, ensure_ascii=False))
        except Exception as exc:
            self._send(500, json.dumps({"error": str(exc)}, ensure_ascii=False))


if __name__ == "__main__":
    print(f"Hjerterom kjører lokalt: http://{HOST}:{PORT}")
    print("Samtaler lagres ikke. Hold dette vinduet åpent mens du bruker assistenten.")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
