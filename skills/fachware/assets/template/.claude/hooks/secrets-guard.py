#!/usr/bin/env python3
"""Härtung für hook-fähige Harnesses: verhindert, dass Secret-Dateien angezeigt
oder committet werden. Die Regel selbst steht in skills/setup/SKILL.md (Schritt 3)
und gilt in jedem Harness; dieses Skript setzt sie dort durch, wo das Harness
PreToolUse-Hooks unterstützt. Antwort per Exit-Code: 0 = erlauben, 2 = blockieren
(Text auf der Fehlerausgabe geht an das Modell). Die Sperre deckt die gängigen Wege
ab und ist mit genug Aufwand umgehbar – sie verstärkt die Regel, sie ersetzt sie nicht."""

import json
import os
import re
import subprocess
import sys

try:
    aufruf = json.load(sys.stdin)
    werkzeug = aufruf.get("tool_name", "")
    eingabe = aufruf.get("tool_input", {}) or {}
    befehl = eingabe.get("command", "")
except Exception:
    sys.exit(0)  # kaputte Eingabe blockiert nichts

# 0. Eingebaute Lese- und Schreibwerkzeuge des Harness (Read, Grep, Edit, Write):
#    kein Zugriff auf Secret-Dateien – der Inhalt würde sonst in den Kontext und damit
#    zum Modellanbieter wandern. Das Werkzeug selbst liest die .env zur Laufzeit; der
#    Agent braucht nur die Variablennamen aus .env.example.
if werkzeug and werkzeug != "Bash":
    pfade = [str(eingabe.get(k, "")) for k in ("file_path", "path", "notebook_path")]
    for pfad in pfade:
        name = pfad.replace("\\", "/").rstrip("/").split("/")[-1]
        if name and re.fullmatch(r"\.env(?!\.example)[.\w-]*", name):
            print("Blockiert: Secret-Dateien werden mit keinem Werkzeug gelesen oder "
                  "bearbeitet – auch nicht mit den eingebauten. Die Variablennamen stehen "
                  "in .env.example; die Werte liest das Werkzeug selbst zur Laufzeit. "
                  "Siehe AGENTS.md, Regel »Secrets«.", file=sys.stderr)
            sys.exit(2)
    sys.exit(0)


def ziel_repo(git_argumente):
    """Repo, auf das ein git-Befehl wirkt: git -C <pfad>, vorangestelltes cd <pfad>, sonst cwd."""
    mc = re.search(r'-C\s+([^\s;|&]+)', git_argumente)
    if mc:
        return os.path.normpath(os.path.join(os.getcwd(), mc.group(1)))
    mcd = re.match(r'\s*cd\s+([^\s;|&]+)\s*(?:&&|;)', befehl)
    if mcd:
        return os.path.normpath(os.path.join(os.getcwd(), mcd.group(1)))
    return os.getcwd()

# .env und ähnliche Secret-Dateien, aber nicht .env.example
SECRET = r'\.env(?!\.example)[.\w-]*'

# Erlaubte Struktur-Prüfung: nur Variablennamen, keine Werte (cut -d= -f1)
SAFE_CUT = re.compile(r"\bcut\s+-d\s*['\"]?=['\"]?\s+-f\s*1\s+[^|;&\n]*")
befehl_pruef = SAFE_CUT.sub(' ', befehl)

# 1. Befehle, die den Inhalt einer Secret-Datei ausgeben würden
ANZEIGE = re.compile(
    r'\b(cat|less|more|head|tail|nl|strings|xxd|od|base64|grep|awk|sed|cut|sort|uniq|column|paste|rev|tac'
    r'|hexdump|dd|jq|bat|pr|fold|python[\d.]*|perl|ruby|node|nodejs|php|lua)\b'
    r'[^|;&\n]*' + SECRET, re.IGNORECASE)
if ANZEIGE.search(befehl_pruef):
    print("Blockiert: Diese Datei kann Secrets enthalten und wird nicht angezeigt. "
          "Erlaubt bleiben Struktur-Prüfungen ohne Werte, etwa wc -l .env oder "
          "cut -d= -f1 .env. Werte per Dateireferenz übertragen – "
          "siehe skills/setup/SKILL.md, Schritt 3.", file=sys.stderr)
    sys.exit(2)

# 1b. Ausgabe von Secret-Variablen (echo $JIRA_API_TOKEN und Verwandte)
VAR_AUSGABE = re.compile(
    r'\b(echo|printf)\b[^|;&\n]*\$\{?\w*(TOKEN|SECRET|KEY|PASS|PWD|CREDENTIAL|AUTH)\w*',
    re.IGNORECASE)
if VAR_AUSGABE.search(befehl):
    print("Blockiert: Diese Variable kann ein Secret enthalten und wird nicht "
          "ausgegeben – auch nicht redigiert. Nutze sie direkt im Aufruf "
          "(etwa als Header), ohne sie anzuzeigen – siehe skills/setup/SKILL.md, "
          "Schritt 3.", file=sys.stderr)
    sys.exit(2)

# 2. Secret-Dateien zum Commit vormerken – namentlich oder pauschal (git add . / -A)
m_add = re.search(r'\bgit\b([^|;&\n]*)\badd\b([^|;&\n]*)', befehl)
if m_add:
    if re.search(SECRET, m_add.group(2)):
        print("Blockiert: .env-Dateien werden nicht committet – sie stehen in .gitignore. "
              "Siehe AGENTS.md, Regel »Secrets«.", file=sys.stderr)
        sys.exit(2)
    if re.search(r'(^|\s)(\.|-A|--all|:/)(\s|$)', m_add.group(2)):
        ziel = ziel_repo(m_add.group(1))
        try:
            for name in os.listdir(ziel):
                if re.fullmatch(SECRET, name):
                    ign = subprocess.run(["git", "-C", ziel, "check-ignore", "-q", name],
                                         capture_output=True, timeout=10)
                    if ign.returncode != 0:
                        print(f"Blockiert: '{name}' liegt im Repo und steht nicht in .gitignore – "
                              "ein pauschales git add würde sie zum Commit vormerken. Trage sie in "
                              ".gitignore ein, dann erneut.", file=sys.stderr)
                        sys.exit(2)
        except Exception:
            pass

# 3. Commit mit bereits vorgemerkter Secret-Datei
m_commit = re.search(r'\bgit\b([^|;&\n]*)\bcommit\b', befehl)
if m_commit:
    try:
        staged = subprocess.run(["git", "-C", ziel_repo(m_commit.group(1)),
                                 "diff", "--cached", "--name-only"],
                                capture_output=True, text=True, timeout=10).stdout
        for zeile in staged.splitlines():
            name = zeile.strip().split("/")[-1]
            if re.fullmatch(SECRET, name):
                print(f"Blockiert: '{zeile.strip()}' ist zum Commit vorgemerkt und kann "
                      "Secrets enthalten. Nimm die Datei aus dem Staging "
                      "(git restore --staged) und prüfe .gitignore.", file=sys.stderr)
                sys.exit(2)
    except Exception:
        pass

sys.exit(0)
