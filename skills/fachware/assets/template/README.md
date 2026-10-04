# {Werkzeugname}

Ein harness-first ausgeliefertes Fachwerkzeug – erzeugt aus dem [Fachware-Template](https://github.com/dittsn/fachware-template).

_Steht hier noch `{Werkzeugname}`, ist dieses Repo frisch aus der Vorlage erzeugt: im Harness öffnen und sagen, was gebraucht wird – der Agent fragt das Nötige und trägt den Namen ein. Konzept, Papier und Spezifikation: [fachware](https://github.com/dittsn/fachware)._

## Benutzen

Dieses Repo in einem Harness öffnen (Claude, Copilot, pi …) und einfach sprechen:

- Noch keine Anforderung? → »Starte das Anforderungsgespräch.«
- Anforderung da, noch nicht eingerichtet? → »Starte die Einrichtung.«
- Läuft schon? → »Führe das Werkzeug aus.« oder »Das Ergebnis passt nicht, lass uns justieren.«

Der Agent erledigt den Rest; seine Regeln stehen in [AGENTS.md](AGENTS.md).

## Härtung für hook-fähige Harnesses

Unter `.claude/` liegen zwei Hooks für Harnesses, die PreToolUse-Hooks unterstützen (Claude Code; die Skripte sind auf andere hook-fähige Harnesses übertragbar): `secrets-guard.py` lehnt Befehle ab, die Secret-Dateien oder Secret-Variablen anzeigen oder committen würden; `tag-guard.py` lehnt Versions-Tags ab, solange die Selbstauskunft nicht ausgefüllt ist. Beide Regeln stehen in den Skills und gelten in jedem Harness – die Hooks setzen sie zusätzlich durch, wo das Harness es kann. Harnesses ohne Hook-Unterstützung ignorieren den Ordner; das Werkzeug funktioniert dort unverändert.

## Stand

- Anforderung: [REQUIREMENT.md](REQUIREMENT.md)
- Konfiguration und Begründungen: [config/config.yaml](config/), [CONFIG.md](CONFIG.md)
- Verbesserungen: [IMPROVEMENTS.md](IMPROVEMENTS.md)
- Selbstauskunft und Meldung: [governance/REGISTRATION.md](governance/REGISTRATION.md)
