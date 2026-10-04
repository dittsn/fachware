#!/usr/bin/env python3
"""Härtung für hook-fähige Harnesses: lehnt das Setzen eines Versions-Tags in einem
Werkzeug-Repo ab, solange dessen Selbstauskunft in governance/REGISTRATION.md nicht
ausgefüllt ist. Die Regel selbst steht in skills/setup/SKILL.md (Schritte 6 bis 8: Testen, Melden, Einfrieren).
Gilt nur für Repos mit governance/-Ordner (Werkzeuge aus dem Template); andere Repos
bleiben unberührt. Ob der Mensch das Ergebnis bestätigt hat, kann dieses Skript nicht
sehen – das bleibt Sache des Gesprächs."""

import json
import os
import re
import sys

try:
    aufruf = json.load(sys.stdin)
    befehl = aufruf.get("tool_input", {}).get("command", "")
except Exception:
    sys.exit(0)

# Nur das ANLEGEN eines Tags prüfen (nicht -l/--list/-d/--delete/-v)
m = re.search(r'\bgit\b([^|;&\n]*)\btag\b([^|;&\n]*)', befehl)
if not m:
    sys.exit(0)
argumente = m.group(2)
if re.search(r'(^|\s)(-l|--list|-d|--delete|-v|--verify)\b', argumente) or not argumente.strip():
    sys.exit(0)

# Ziel-Repo bestimmen: git -C <pfad> oder vorangestelltes cd <pfad>, sonst Arbeitsverzeichnis
ziel = os.getcwd()
mc = re.search(r'-C\s+([^\s;|&]+)', m.group(1))
if mc:
    ziel = os.path.normpath(os.path.join(os.getcwd(), mc.group(1)))
else:
    mcd = re.match(r'\s*cd\s+([^\s;|&]+)\s*(?:&&|;)', befehl)
    if mcd:
        ziel = os.path.normpath(os.path.join(os.getcwd(), mcd.group(1)))

gov = os.path.join(ziel, "governance")
if not os.path.isdir(gov):
    sys.exit(0)  # kein Werkzeug-Repo aus dem Template – nicht zuständig

pfad = os.path.join(gov, "REGISTRATION.md")
grund = None
if not os.path.exists(pfad):
    grund = "governance/REGISTRATION.md existiert nicht."
else:
    inhalt = open(pfad, encoding="utf-8").read()
    zeilen = inhalt.splitlines()
    leere_felder = []
    for i, z in enumerate(zeilen):
        m_feld = re.match(r'^\s*-\s*\*\*([^*]+?):?\*\*', z)
        if not m_feld:
            continue
        name = m_feld.group(1).strip()
        # Kommentare und Fettung entfernen; der letzte Doppelpunkt trennt Feldkopf und Wert
        klar = re.sub(r'<!--.*?-->', '', z).replace("**", "").strip()
        kopf, doppelpunkt, dahinter = klar.rpartition(":")
        if not doppelpunkt:
            continue  # keine Feldzeile
        if dahinter.strip():
            continue  # Wert steht in derselben Zeile
        # Mehrzeilige Felder (etwa Datenzugriffe): eingerückte Folgezeilen zählen als Inhalt
        gefuellt = False
        for folge in zeilen[i + 1:]:
            if not folge.strip():
                continue
            gefuellt = folge[:1] in (" ", "\t")
            break
        if not gefuellt:
            leere_felder.append(name)
    if leere_felder:
        grund = "diese Felder der Selbstauskunft sind leer: " + "; ".join(leere_felder[:6]) + (" …" if len(leere_felder) > 6 else "")
if grund:
    print("Blockiert: Der Tag setzt die ausgefüllte Selbstauskunft voraus – " + grund +
          " Fülle governance/REGISTRATION.md aus (Angaben zu Personen nur aus Antworten "
          "des Menschen, Unbekanntes ausdrücklich als unbekannt) und lass den Menschen "
          "das Ergebnis vorher bestätigen – siehe skills/setup/SKILL.md, Schritte 6 bis 8.",
          file=sys.stderr)
    sys.exit(2)
sys.exit(0)
