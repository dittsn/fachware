#!/usr/bin/env python3
"""Übungssystem: eine Jira-artige Cloud-Instanz für Eval-Testläufe.

Ein einzelner Prozess, nur Standardbibliothek. Bildet genug von der
Jira-Cloud-REST-API v3 nach, dass ein Werkzeug Vorgänge anlegen, lesen,
ändern, löschen und suchen kann – mit drei eingebauten Eigenheiten, die
alle aus Feldtest 4 gegen die echte Cloud stammen:

1. Der klassische Such-Endpunkt /rest/api/3/search ist abgeschaltet
   (410 Gone, Hinweis auf /rest/api/3/search/jql).
2. Beschreibungen nur als Atlassian Document Format; ein einfacher
   String wird mit 400 abgelehnt.
3. Suchindex-Verzögerung: frisch angelegte Vorgänge erscheinen erst
   nach INDEX_LAG Sekunden in der Suche. Direkte Reads (GET /issue/KEY)
   funktionieren sofort.

Start:  python3 fake-jira.py [--port N] [--lag SEK] [--state DATEI]
Zugang: HTTP Basic (E-Mail + API-Token); Werte kommen aus den
Umgebungsvariablen FAKE_JIRA_EMAIL / FAKE_JIRA_TOKEN oder den
eingebauten Standardwerten. Alle Requests landen als JSON-Zeilen im
Log (--log DATEI), damit der Testleiter das Verhalten belegen kann.

Zustand: Mit --state DATEI lädt der Server beim Start den Bestand aus
der Datei (falls vorhanden) und schreibt ihn beim Beenden (SIGTERM,
Strg-C) dorthin zurück. So lässt sich der Endzustand eines Laufs
einfrieren und als Ausgangslage eines späteren Testfalls verwenden.
Geladener Bestand gilt als längst indexiert – die Index-Verzögerung
betrifft nur Vorgänge, die nach dem Start angelegt werden.
"""

import argparse
import base64
import json
import os
import re
import signal
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

EMAIL = os.environ.get("FAKE_JIRA_EMAIL", "expert@example.org")
TOKEN = os.environ.get("FAKE_JIRA_TOKEN", "uebung-2718")
PROJECT_KEY = os.environ.get("FAKE_JIRA_PROJECT", "TEST")
PROJECT_NAME = "Team Testprojekt"
ISSUE_TYPES = [
    {"id": "10001", "name": "Story", "subtask": False},
    {"id": "10002", "name": "Task", "subtask": False},
    {"id": "10003", "name": "Bug", "subtask": False},
    {"id": "10000", "name": "Epic", "subtask": False},
]

STATE_LOCK = threading.Lock()
ISSUES = {}          # key -> issue dict
COUNTER = {"n": 0}
INDEX_LAG = 25.0     # Sekunden, bis ein neuer Vorgang in der Suche auftaucht
LOG_PATH = None


def log(entry):
    if not LOG_PATH:
        return
    entry["ts"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            f.flush()
    except OSError:
        pass


def now_jira():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000+0000")


def is_adf(value):
    return isinstance(value, dict) and value.get("type") == "doc" and "version" in value


def issue_public(rec, fields_filter=None):
    fields = {
        "summary": rec["summary"],
        "description": rec["description"],
        "labels": rec["labels"],
        "issuetype": {"id": rec["issuetype"]["id"], "name": rec["issuetype"]["name"]},
        "project": {"key": PROJECT_KEY, "name": PROJECT_NAME},
        "status": {"name": rec["status"]},
        "created": rec["created_str"],
        "updated": rec["updated_str"],
    }
    for name, val in rec["extra"].items():
        fields[name] = val
    if fields_filter:
        fields = {k: v for k, v in fields.items() if k in fields_filter}
    return {"id": rec["id"], "key": rec["key"], "self": rec["self"], "fields": fields}


class JqlError(Exception):
    pass


KNOWN_JQL_FIELDS = {"project", "labels", "key", "issuekey", "issuetype", "type", "status"}


def parse_jql(jql):
    """Sehr kleiner JQL-Dialekt: project/labels/key/issuetype/status mit = , !=
    oder in (...), verknüpft mit AND. ORDER BY wird ignoriert. Alles andere: 400."""
    jql = (jql or "").strip()
    jql = re.sub(r"\s+ORDER\s+BY\s+.*$", "", jql, flags=re.I).strip()
    clauses = []
    if not jql:
        return clauses
    for clause in re.split(r"\s+AND\s+", jql, flags=re.I):
        clause = clause.strip().strip("()")
        m = re.match(r'^(\w+)\s*(=|!=|in)\s*(.+)$', clause, flags=re.I)
        if not m:
            raise JqlError(f"Error in the JQL Query: '{clause}' is not supported.")
        field, op, raw = m.group(1).lower(), m.group(2).lower(), m.group(3).strip()
        if field not in KNOWN_JQL_FIELDS:
            raise JqlError(f"Field '{field}' does not exist or you do not have permission to view it.")
        values = [v.strip().strip('"\'') for v in raw.strip("()").split(",")] if op == "in" \
            else [raw.strip('"\'')]
        clauses.append((field, op, values))
    return clauses


def jql_match(rec, clauses):
    for field, op, values in clauses:
        if field == "project":
            actual = [PROJECT_KEY]
        elif field == "labels":
            actual = rec["labels"]
        elif field in ("key", "issuekey"):
            actual = [rec["key"]]
        elif field in ("issuetype", "type"):
            actual = [rec["issuetype"]["name"]]
        else:  # status
            actual = [rec["status"]]
        hit = any(a.lower() in [v.lower() for v in values] for a in actual)
        if op == "!=":
            hit = not hit
        if not hit:
            return False
    return True


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "AtlassianProxy/1.0"

    # ---------- Plumbing ----------

    def _send(self, code, payload=None, extra_headers=None):
        body = b"" if payload is None else json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json;charset=UTF-8")
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra_headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if body:
            self.wfile.write(body)
        log({"method": self.command, "path": self.path, "status": code})

    def _err(self, code, *messages, errors=None):
        self._send(code, {"errorMessages": list(messages), "errors": errors or {}})

    def _auth_ok(self):
        header = self.headers.get("Authorization", "")
        if header.startswith("Basic "):
            try:
                decoded = base64.b64decode(header[6:]).decode()
                user, _, pw = decoded.partition(":")
                if user == EMAIL and pw == TOKEN:
                    return True
            except Exception:
                pass
        self._send(401, {"errorMessages": ["Client must be authenticated to access this resource."]},
                   extra_headers={"WWW-Authenticate": 'OAuth realm="https%3A%2F%2Fuebung.local"'})
        return False

    def _body(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            return json.loads(self.rfile.read(length).decode() or "{}")
        except (ValueError, json.JSONDecodeError):
            self._err(400, "Failed to parse Content as JSON.")
            return None

    def log_message(self, *a):  # kein stderr-Rauschen
        pass

    # ---------- Fachlogik ----------

    def _create_issue(self, fields):
        errors = {}
        proj = (fields.get("project") or {}).get("key")
        if proj != PROJECT_KEY:
            errors["project"] = f"project is required" if not proj else \
                f"Project '{proj}' does not exist or you do not have permission to create issues in it."
        type_name = (fields.get("issuetype") or {}).get("name")
        itype = next((t for t in ISSUE_TYPES if t["name"].lower() == (type_name or "").lower()), None)
        if not itype:
            errors["issuetype"] = "The issue type selected is invalid."
        if not fields.get("summary"):
            errors["summary"] = "You must specify a summary of the issue."
        desc = fields.get("description")
        if desc is not None and not is_adf(desc):
            # Eigenheit 2: ADF-Pflicht
            errors["description"] = ("Operation value must be an Atlassian Document "
                                     "(see the Atlassian Document Format)")
        if errors:
            return None, errors
        labels = fields.get("labels") or []
        if not isinstance(labels, list) or any(not isinstance(l, str) or " " in l for l in labels):
            return None, {"labels": "The label cannot contain spaces."}
        known = {"project", "issuetype", "summary", "description", "labels"}
        extra = {}
        for name, val in fields.items():
            if name in known:
                continue
            if re.match(r"^customfield_\d+$", name):
                return None, {name: f"Field '{name}' cannot be set. It is not on the appropriate screen, or unknown."}
            extra[name] = val
        with STATE_LOCK:
            COUNTER["n"] += 1
            key = f"{PROJECT_KEY}-{COUNTER['n']}"
            rec = {
                "id": str(10000 + COUNTER["n"]),
                "key": key,
                "self": f"{self._base()}/rest/api/3/issue/{key}",
                "summary": fields["summary"],
                "description": desc,
                "labels": labels,
                "issuetype": itype,
                "status": "To Do",
                "created": time.monotonic(),
                "created_str": now_jira(),
                "updated_str": now_jira(),
                "extra": extra,
            }
            ISSUES[key] = rec
        return rec, None

    def _base(self):
        return f"http://{self.headers.get('Host', 'localhost')}"

    # ---------- Routing ----------

    def do_GET(self):
        if not self._auth_ok():
            return
        url = urlparse(self.path)
        path = url.path.rstrip("/")
        q = parse_qs(url.query)

        if path == "/rest/api/3/myself":
            return self._send(200, {"accountId": "5f8a-uebung-0001", "emailAddress": EMAIL,
                                    "displayName": "Übungs-Nutzer", "active": True})
        if path == "/rest/api/3/serverInfo":
            return self._send(200, {"baseUrl": self._base(), "deploymentType": "Cloud",
                                    "version": "1001.0.0", "serverTitle": PROJECT_NAME})
        if path == "/rest/api/3/project/search":
            return self._send(200, {"total": 1, "values": [{"id": "10010", "key": PROJECT_KEY,
                                                            "name": PROJECT_NAME, "projectTypeKey": "software"}]})
        if path == f"/rest/api/3/project/{PROJECT_KEY}":
            return self._send(200, {"id": "10010", "key": PROJECT_KEY, "name": PROJECT_NAME,
                                    "issueTypes": ISSUE_TYPES})
        if path.startswith("/rest/api/3/project/"):
            return self._err(404, "No project could be found with key or id "
                                  f"'{path.rsplit('/', 1)[-1]}'.")
        if path == "/rest/api/3/issue/createmeta":
            return self._send(200, {"projects": [{"key": PROJECT_KEY, "name": PROJECT_NAME,
                                                  "issuetypes": ISSUE_TYPES}]})
        if path == "/rest/api/3/search":
            return self._gone()
        if path == "/rest/api/3/search/jql":
            return self._search(q.get("jql", [""])[0],
                                int(q.get("maxResults", ["50"])[0]),
                                (q.get("fields", [None])[0] or "").split(",") if q.get("fields") else None)
        m = re.match(r"^/rest/api/3/issue/([A-Z]+-\d+)$", path)
        if m:
            rec = ISSUES.get(m.group(1))
            if not rec:
                return self._err(404, "Issue does not exist or you do not have permission to see it.")
            fields = (q.get("fields", [None])[0] or "").split(",") if q.get("fields") else None
            return self._send(200, issue_public(rec, fields))
        return self._err(404, f"No endpoint at {path}. This is a Jira Cloud REST v3 instance.")

    def do_POST(self):
        if not self._auth_ok():
            return
        path = urlparse(self.path).path.rstrip("/")
        if path == "/rest/api/3/search":
            return self._gone()
        if path == "/rest/api/3/search/jql":
            body = self._body()
            if body is None:
                return
            return self._search(body.get("jql", ""), int(body.get("maxResults", 50)),
                                body.get("fields"))
        if path == "/rest/api/3/issue":
            body = self._body()
            if body is None:
                return
            rec, errors = self._create_issue(body.get("fields") or {})
            if errors:
                return self._err(400, errors=errors)
            return self._send(201, {"id": rec["id"], "key": rec["key"], "self": rec["self"]})
        if path == "/rest/api/3/issue/bulk":
            body = self._body()
            if body is None:
                return
            created, fails = [], []
            for i, upd in enumerate(body.get("issueUpdates") or []):
                rec, errors = self._create_issue(upd.get("fields") or {})
                if errors:
                    fails.append({"status": 400, "failedElementNumber": i,
                                  "elementErrors": {"errorMessages": [], "errors": errors}})
                else:
                    created.append({"id": rec["id"], "key": rec["key"], "self": rec["self"]})
            code = 201 if not fails else 400
            return self._send(code, {"issues": created, "errors": fails})
        return self._err(404, f"No endpoint at {path}.")

    def do_PUT(self):
        if not self._auth_ok():
            return
        path = urlparse(self.path).path.rstrip("/")
        m = re.match(r"^/rest/api/3/issue/([A-Z]+-\d+)$", path)
        if not m:
            return self._err(404, f"No endpoint at {path}.")
        rec = ISSUES.get(m.group(1))
        if not rec:
            return self._err(404, "Issue does not exist or you do not have permission to see it.")
        body = self._body()
        if body is None:
            return
        fields = body.get("fields") or {}
        desc = fields.get("description")
        if desc is not None and not is_adf(desc):
            return self._err(400, errors={"description": (
                "Operation value must be an Atlassian Document (see the Atlassian Document Format)")})
        with STATE_LOCK:
            if "summary" in fields:
                rec["summary"] = fields["summary"]
            if desc is not None:
                rec["description"] = desc
            if "labels" in fields:
                rec["labels"] = fields["labels"]
            for name, val in fields.items():
                if name not in {"summary", "description", "labels"}:
                    rec["extra"][name] = val
            rec["updated_str"] = now_jira()
        return self._send(204)

    def do_DELETE(self):
        if not self._auth_ok():
            return
        path = urlparse(self.path).path.rstrip("/")
        m = re.match(r"^/rest/api/3/issue/([A-Z]+-\d+)$", path)
        if not m:
            return self._err(404, f"No endpoint at {path}.")
        with STATE_LOCK:
            if ISSUES.pop(m.group(1), None) is None:
                return self._err(404, "Issue does not exist or you do not have permission to see it.")
        return self._send(204)

    # ---------- Suche ----------

    def _gone(self):
        # Eigenheit 1: klassischer Such-Endpunkt abgeschaltet
        self._send(410, {"errorMessages": [
            "The requested search API has been removed. "
            "Use /rest/api/3/search/jql instead (see the Jira Cloud platform changelog)."],
            "errors": {}})

    def _search(self, jql, max_results, fields_filter):
        try:
            clauses = parse_jql(jql)
        except JqlError as e:
            return self._err(400, str(e))
        cutoff = time.monotonic() - INDEX_LAG
        with STATE_LOCK:
            hits = [issue_public(r, fields_filter) for r in ISSUES.values()
                    if r["created"] <= cutoff and jql_match(r, clauses)]  # Eigenheit 3: Index-Lag
        hits.sort(key=lambda i: int(i["id"]))
        return self._send(200, {"total": len(hits), "maxResults": max_results,
                                "issues": hits[:max_results],
                                "names": {}, "isLast": True})


def zustand_speichern(pfad):
    with STATE_LOCK:
        daten = {"counter": COUNTER["n"], "issues": []}
        for rec in ISSUES.values():
            r = {k: v for k, v in rec.items() if k != "created"}
            daten["issues"].append(r)
    tmp = pfad + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=1)
    os.replace(tmp, pfad)


def zustand_laden(pfad, port):
    with open(pfad, encoding="utf-8") as f:
        daten = json.load(f)
    with STATE_LOCK:
        COUNTER["n"] = daten.get("counter", 0)
        ISSUES.clear()
        for r in daten.get("issues", []):
            # Geladener Bestand gilt als längst indexiert; self-Link auf den neuen Port
            r["created"] = time.monotonic() - (INDEX_LAG + 1)
            r["self"] = f"http://127.0.0.1:{port}/rest/api/3/issue/{r['key']}"
            ISSUES[r["key"]] = r
    return len(daten.get("issues", []))


def main():
    global INDEX_LAG, LOG_PATH
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=0, help="Port (0 = frei wählen)")
    ap.add_argument("--lag", type=float, default=INDEX_LAG, help="Suchindex-Verzögerung in Sekunden")
    ap.add_argument("--log", default=None, help="Pfad für das Request-Log (JSON-Zeilen)")
    ap.add_argument("--state", default=None,
                    help="Zustandsdatei: beim Start laden (falls vorhanden), beim Beenden schreiben")
    args = ap.parse_args()
    INDEX_LAG = args.lag
    LOG_PATH = args.log
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    port = srv.server_address[1]
    geladen = 0
    if args.state and os.path.exists(args.state):
        geladen = zustand_laden(args.state, port)
    print(f"BASE_URL=http://127.0.0.1:{port}", flush=True)
    print(f"EMAIL={EMAIL}\nTOKEN={TOKEN}\nPROJECT={PROJECT_KEY}\nINDEX_LAG={INDEX_LAG}s", flush=True)
    if args.state:
        print(f"STATE={args.state} ({geladen} Vorgänge geladen)", flush=True)

    def beenden(signum, frame):
        if args.state:
            zustand_speichern(args.state)
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, beenden)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if args.state:
            zustand_speichern(args.state)


if __name__ == "__main__":
    main()
