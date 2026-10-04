# Spezifikation: Repo-Anatomie

Die Bauform eines harness-first ausgelieferten Werkzeugs. Das Template im Skill (`skills/fachware/assets/template/`) setzt sie um; dasselbe Template liegt als eigenständiges Repo `dittsn/fachware-template` vor (per Ausspielung, gleiche Versions-Tags) und ist der Startpunkt per »Use this template«.

| Pfad | Zweck | Pflicht |
| --- | --- | --- |
| `AGENTS.md` | Verhalten des Harness: Phasenlogik, Regeln, Verbote | MUSS |
| `skills/requirements/SKILL.md` | Phase 1: Anforderungsgespräch | SOLL |
| `skills/setup/SKILL.md` | Phase 2: Einrichtungsgespräch | MUSS |
| `skills/improve/SKILL.md` | Phase 3: Verbesserungsdialog | SOLL |
| `REQUIREMENT.md` | Ergebnis Phase 1: die fachliche Anforderung, versioniert | MUSS |
| `config/config.yaml` | Maschinenlesbare Konfiguration | MUSS |
| `CONFIG.md` | Begründungen: warum welche Quelle wofür gewählt wurde | MUSS |
| `IMPROVEMENTS.md` | Verbesserungslog aus Phase 3 | SOLL |
| `governance/REGISTRATION.md` | Selbstauskunft und Meldestatus fürs Tool-/IDV-Verzeichnis | MUSS |
| `src/` | Der kristallisierte Kern: deterministisch, getestet, versioniert | MUSS |
| `.env` (Vorlage: `.env.example`) | Secrets lokal; `.env` per `.gitignore` ausgeschlossen | MUSS |
| `.claude/` (settings.json, hooks/) | Härtung für hook-fähige Harnesses: blockiert Secret-Anzeige und Tag ohne Selbstauskunft; die Regeln selbst stehen in den Skills | KANN |

Grundsatz: Jede Phase hinterlässt ihr Artefakt im Repo. Das Repo ist damit zugleich Werkzeug, Dokumentation und Audit-Trail.
