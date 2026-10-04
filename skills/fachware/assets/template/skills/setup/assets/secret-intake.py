#!/usr/bin/env python3
"""Lokale Eingabeseite für Secrets (Out-of-Band-Übergabe).

Vom Werkzeug-Ordner aus starten:  python3 skills/setup/assets/secret-intake.py
Liest die Variablennamen aus .env.example, zeigt unter der beim Start
ausgegebenen Adresse (zufälliger Port, zufälliger Pfad) ein Formular und
schreibt die Eingaben beim Speichern direkt in ./.env. Anfragen ohne den
zufälligen Pfad, mit fremdem Host-Header oder fremdem Origin werden
abgewiesen – damit keine fremde Webseite den Speichern-Aufruf auslösen kann.
Die Werte laufen nie durch das Gespräch oder den Kontext des Agenten.

Funktioniert nur, wenn Harness und Browser auf derselben Maschine laufen –
aus einem Container ohne Port-Freigabe ist die Seite nicht erreichbar.
Bindet ausschließlich an 127.0.0.1 und beendet sich nach dem Speichern.

Übergangslösung: Dieses Formular überbrückt die fehlende Plattformschicht
für Berechtigungen. Sobald verwaltete Anbindungen mit Browser-Login (etwa
OAuth im MCP-Standard) den Zugang übernehmen, entfällt es.
"""
import html
import os
import random
import re
import secrets
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else random.randint(49152, 65535)
PATH_TOKEN = secrets.token_urlsafe(16)
ENV_EXAMPLE = ".env.example"
ENV_FILE = ".env"
VAR_RE = re.compile(r"^\s*#?\s*([A-Za-z_][A-Za-z0-9_]*)=")


def container_hint():
    """Anzeichen dafür, dass dieser Prozess in einem Container läuft (None = keins gefunden)."""
    if sys.platform == "darwin":
        return None
    if os.path.exists("/.dockerenv"):
        return "/.dockerenv vorhanden (Docker)"
    if os.path.exists("/run/.containerenv"):
        return "/run/.containerenv vorhanden (Podman)"
    if os.environ.get("container"):
        return "Umgebungsvariable container=" + os.environ["container"]
    try:
        out = subprocess.run(["systemd-detect-virt", "--container"],
                             capture_output=True, text=True, timeout=2)
        virt = out.stdout.strip()
        if out.returncode == 0 and virt and virt != "none":
            return "systemd-detect-virt meldet: " + virt
    except Exception:
        pass
    try:
        with open("/proc/1/cgroup", encoding="utf-8") as fh:
            cg = fh.read()
        if any(k in cg for k in ("docker", "containerd", "kubepods", "lxc")):
            return "/proc/1/cgroup deutet auf einen Container"
    except Exception:
        pass
    return None


def read_fields():
    plain, commented = [], []
    try:
        with open(ENV_EXAMPLE, encoding="utf-8") as f:
            for line in f:
                m = VAR_RE.match(line)
                if not m:
                    continue
                name = m.group(1)
                target = commented if line.lstrip().startswith("#") else plain
                if name not in target:
                    target.append(name)
    except FileNotFoundError:
        pass
    return plain or commented


def page(body):
    return ("<!doctype html><html lang=\"de\"><head><meta charset=\"utf-8\">"
            "<title>Zugangsdaten eintragen</title>"
            "<style>body{font-family:sans-serif;max-width:40rem;margin:3rem auto;"
            "padding:0 1rem;line-height:1.5}input{width:100%;padding:.5rem;"
            "margin:.25rem 0 1rem;font-family:monospace}button{padding:.6rem 1.2rem}"
            "p.note{color:#555;font-size:.9rem}</style></head><body>" + body +
            "</body></html>").encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # keine Request-Logs (Pfade genügen nicht, Werte nie)
        pass

    def _reject(self, code, msg):
        data = page(f"<h1>{msg}</h1>")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _guard(self, need_origin=False):
        """True, wenn die Anfrage abgelehnt wurde."""
        allowed_hosts = {f"127.0.0.1:{PORT}", f"localhost:{PORT}"}
        if self.headers.get("Host") not in allowed_hosts:
            self._reject(403, "Abgelehnt: fremder Host-Header"); return True
        origin = self.headers.get("Origin")
        allowed_origins = {f"http://{h}" for h in allowed_hosts}
        if origin and origin not in allowed_origins:
            self._reject(403, "Abgelehnt: fremder Origin"); return True
        if need_origin and origin is None and self.headers.get("Referer") is None:
            self._reject(403, "Abgelehnt: Herkunft unklar"); return True
        return False

    def do_GET(self):
        if self.path.rstrip("/") != f"/{PATH_TOKEN}":
            self._reject(404, "Nicht gefunden"); return
        if self._guard():
            return
        fields = read_fields()
        if not fields:
            inner = "<h1>Keine Variablen gefunden</h1><p>In .env.example stehen keine Einträge der Form NAME=.</p>"
        else:
            inputs = "".join(
                f"<label for=\"{html.escape(n)}\">{html.escape(n)}</label>"
                f"<input id=\"{html.escape(n)}\" name=\"{html.escape(n)}\" autocomplete=\"off\" spellcheck=\"false\">"
                for n in fields)
            inner = ("<h1>Zugangsdaten eintragen</h1>"
                     "<p>Diese Seite kommt von einem Mini-Server auf deinem eigenen Rechner (127.0.0.1). "
                     "Beim Speichern werden die Eingaben direkt in die Datei <code>.env</code> im Werkzeug-Ordner "
                     "geschrieben und nirgendwohin gesendet – auch nicht an das Harness oder in den Chat.</p>"
                     f"<form method=\"post\" action=\"/{PATH_TOKEN}/save\">{inputs}"
                     "<button type=\"submit\">Speichern und beenden</button></form>"
                     "<p class=\"note\">Leer gelassene Felder bleiben unangetastet.</p>"
                     "<p class=\"note\">Hinweis: Das funktioniert nur, wenn das Harness auf demselben Rechner läuft "
                     "wie dieser Browser. Läuft das Harness in einem Container oder auf einer anderen Maschine, "
                     "ist diese Seite von dort nicht erreichbar – dann muss die .env von Hand ausgefüllt werden.</p>")
        data = page(inner)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != f"/{PATH_TOKEN}/save":
            self._reject(404, "Nicht gefunden"); return
        if self._guard(need_origin=True):
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self._reject(400, "Ungültige Anfrage"); return
        if length > 65536:
            self._reject(413, "Abgelehnt: Anfrage zu groß"); return
        try:
            submitted = parse_qs(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            self._reject(400, "Ungültige Anfrage"); return
        values = {k: v[0] for k, v in submitted.items() if v and v[0].strip()}
        known = set(read_fields())
        values = {k: v for k, v in values.items() if k in known}
        if any("\n" in v or "\r" in v for v in values.values()):
            self._reject(400, "Abgelehnt: Werte dürfen keine Zeilenumbrüche enthalten"); return

        kept = []
        if os.path.exists(ENV_FILE):
            with open(ENV_FILE, encoding="utf-8") as f:
                for line in f:
                    m = VAR_RE.match(line)
                    if not (m and not line.lstrip().startswith("#") and m.group(1) in values):
                        kept.append(line.rstrip("\n"))
        for name, value in values.items():
            kept.append(f"{name}={value}")
        # Atomar schreiben: erst Temporärdatei mit Modus 600, dann ersetzen
        tmp = ENV_FILE + ".tmp"
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("\n".join(kept) + "\n")
        os.replace(tmp, ENV_FILE)
        os.chmod(ENV_FILE, 0o600)

        data = page(f"<h1>Gespeichert</h1><p>{len(values)} Wert(e) in <code>.env</code> geschrieben. "
                    "Du kannst dieses Fenster schließen und im Gespräch weitermachen – der Server hier beendet sich jetzt.</p>")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        threading.Thread(target=self.server.shutdown, daemon=True).start()


if __name__ == "__main__":
    hint = container_hint()
    if hint:
        print("WARNUNG: Dieser Prozess läuft vermutlich in einem Container (" + hint + ").", flush=True)
        print("Die Eingabeseite ist vom Browser des Menschen dann wahrscheinlich NICHT erreichbar,")
        print("außer ein Port-Mapping existiert. Sonst: .env von Hand ausfüllen.")
    httpd = HTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://127.0.0.1:{PORT}/{PATH_TOKEN}/"
    # OSC-8-Hyperlink für Terminals, die es können; alle anderen zeigen die nackte URL.
    print("Eingabeseite (beendet sich nach dem Speichern):", flush=True)
    print(f"\033]8;;{url}\033\\{url}\033]8;;\033\\", flush=True)
    httpd.serve_forever()
    print("Gespeichert, Server beendet.")
