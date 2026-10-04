# Changelog

## v0.5.0 – 2026-10-03

- Das Muster heißt »Fachware«; »harness-first ausgeliefert« beschreibt den Mechanismus. Neues Repo `dittsn/fachware` mit frischer Historie
- Template als eigenes GitHub-Template-Repo `dittsn/fachware-template`: ein Repo pro Werkzeug per »Use this template«; das Template erkennt den frisch erzeugten Zustand und stellt die Eröffnungsfragen selbst; Ausspielung aus diesem Repo per `scripts/template-ausspielen.sh`
- Skill-Ordner `skills/harness-first` heißt jetzt `skills/fachware`; Papier liegt unter `paper/fachware.md`
- AGENTS.md: Das geöffnete Repo ist der Auftrag – jede fachliche Aufgabe läuft über die Skills, ohne Ausnahme; fachliche Inhalte nie stillschweigend verändern; Dateien mit den Harness-Werkzeugen lesen statt über die Shell
- Setup-Skill: Schritt 9 erklärt die Alltagsbenutzung; Akzeptanzkriterien mindestens eines, keine Obergrenze
- Hooks: Pfade über `$CLAUDE_PROJECT_DIR`, damit sie nach Verzeichniswechseln greifen (Defekt aus Suite-Lauf 7); secrets-guard, tag-guard und Eingabeseite nach externem Review gehärtet
- Eval: zweistufige Bewertung mit deterministischem Prüfer `eval/pruefung.py`; Übungssystem mit Zustandsdatei (`--state`); Testfall 06 gegen den eingefrorenen Endzustand von Testfall 05; neuer Testfall 07 »Aufgabe statt Werkzeugwunsch«; Suite-Lauf 7 ausgewertet
- Private Konto-Mailadresse in allen Eval-Dateien redigiert

## v0.4.0 – 2026-09-29

- Eval-Suite in `eval/` in main aufgenommen: sechs Testfälle, sechs Suite-Läufe mit Transkripten und Ergebnissen, Übungssystem (Jira-Imitat) für Testfall 05
- Bewertungsraster zweigeteilt: Regeltreue und Kompetenz getrennt, dazu ein eigener Nachbesserungs-Block; Kriteriennamen ausgeschrieben
- Zwei Testfälle entfernt (»Leg einfach los«, »Korrektur nach Fehlstart«), übrige neu nummeriert; Zuordnungstabelle im Protokoll
- Owner-Regel im Skill: Owner mit Name und Kontaktadresse wird erfragt, nichts aus der Harness-Umgebung übernommen – schließt das Identitätsleck aus Suite-Lauf 4
- Bestätigungs-Regel im Template-Skill: Einfrieren erst nach Bestätigung des Menschen – hob das Reihenfolge-Kriterium von einem bestandenen Lauf von sechs auf drei von drei
- Hooks in `.claude/` (Template und Rahmen-Repo): Secrets-Anzeige und Tag ohne ausgefüllte Selbstauskunft werden blockiert
- DORA-Abgleich als eigene Spezifikation `spec/dora.md` mit Zuordnungstabelle, Deltas für den Finanzkontext und Prüfregel für Änderungen

## v0.3.0 – 2026-09-27

Nach drei Feldtests gehärtet: harte Gesprächs-Gates in allen Skills (Fragen einzeln, warten, nichts erfinden); Setup Schritt 1 verlangt geprüfte statt behaupteter Umgebung und aktive Suche nach MCP-Server/API mit konkretem Vorschlag; Setup Schritt 3 und AGENTS.md verbieten die Ausgabe von Secret-Dateien (nur Struktur prüfen, Werte per Dateireferenz). Papier ergänzt um den Modellqualitäts-Befund, die ungelöste Token-Übergabe und den ersten vollständigen Durchlauf (Werkzeug bis v1.0.0 eingefroren, Selbstauskunft ausgefüllt).

## v0.2.0 – 2026-09-26

Rollen getrennt: Der Bau von Werkzeugen ist jetzt ein installierbarer Skill (`skills/fachware/`, Template als Teil des Skills). `workbench/` und der create-Skill entfallen; Werkzeuge entstehen von Beginn an am Ort der Wahl – im Repo oder überall, wenn der Skill im Harness installiert ist.

## v0.1.0 – 2026-09-26

Erstveröffentlichung: Positionspapier, Spezifikation (Auslieferungsmodell, Repo-Anatomie, Drei-Phasen-Lebenszyklus, Governance), Explain-Skill und Werkzeug-Template.
