# Fachware

**Fachwerkzeuge als Repo: installiert im Gespräch, betrieben im Harness.**

Von [Sebastian Dittmann](https://github.com/dittsn) ([LinkedIn](https://www.linkedin.com/in/sebastian-dittmann/)) · September 2026 · [Positionspapier](paper/fachware.md)

## Die Idee in fünf Sätzen

Harnesses – Claude Desktop, GitHub Copilot, pi und Verwandte – werden für hochgradig individualisierte Fachapplikationen das, was der App Store für Apps war: der Kanal, der eine ganze Softwareklasse vom Sonderfall zur Selbstverständlichkeit macht. Nur ist das Regal diesmal ein Git-Repository und der Installateur ein Gespräch. Ein Werkzeug wird geklont, im Harness geöffnet und rein fachlich eingerichtet: Der Agent fragt, schaut in den Quellsystemen nach, schreibt die Konfiguration und passt sie fortlaufend an. Secrets bleiben auf der Maschine, das Modell kann lokal laufen. Adressiert sind Fachleute, die nicht vibe-coden wollen – und Werkzeuge, die weder Server noch IT-Ressourcen binden sollen.

*English abstract:* Fachware is a pattern for delivering highly individualized domain tools: shipped as a Git repository built for coding harnesses, installed through a purely domain-level conversation (typed or spoken), operated locally with secrets — and optionally the model — on the user's machine. It sits between SaaS (finished but generic) and vibe coding (individual but self-built): finished software that adapts itself in dialogue.

## Zwei Repos, klare Rollen

| Repo | Für wen | Inhalt |
| --- | --- | --- |
| **fachware** (dieses) | Leser und Mitwirkende | Papier, Spezifikation, Skills, Testsuite – und die Quelle des Templates |
| [**fachware-template**](https://github.com/dittsn/fachware-template) | Fachleute, die ein Werkzeug brauchen | Die Vorlage für ein einzelnes Fachwerkzeug: per »Use this template« entsteht ein eigenes Repo, das im Harness geöffnet und im Gespräch eingerichtet wird |

Das Template wird nur hier gepflegt (`skills/fachware/assets/template/`) und per `scripts/template-ausspielen.sh` in das Template-Repo ausgespielt; beide tragen dieselben Versions-Tags. Jedes erzeugte Werkzeug ist ein eigenes Repo – es gibt kein Meta-Repo, in dem gearbeitet wird.

## Was liegt hier

| Pfad | Inhalt |
| --- | --- |
| [paper/](paper/fachware.md) | Das Positionspapier: These, Muster, was neu ist und wo die Grenzen liegen |
| [spec/](spec/delivery-model.md) | Die Spezifikation: Auslieferungsmodell, Repo-Anatomie, Drei-Phasen-Lebenszyklus, Governance |
| [skills/explain/](skills/explain/SKILL.md) | Skill: Dieses Repo erklärt sich selbst im Harness |
| [skills/fachware/](skills/fachware/SKILL.md) | Der installierbare Skill: baut Fachwerkzeuge direkt im Harness – Template inklusive (Quelle für fachware-template) |
| [scripts/](scripts/template-ausspielen.sh) | Ausspielung des Templates in das Template-Repo |
| [eval/](eval/README.md) | Die Testsuite: Testfälle für die Installations-Gespräche, Feldtest-Protokoll, Ergebnisse |
| [skills/eval/](skills/eval/SKILL.md) | Skill: führt die Testsuite im jeweiligen Harness aus |

## Ein Werkzeug bekommen

**Der Standardweg:** Bei [fachware-template](https://github.com/dittsn/fachware-template) »Use this template« drücken, dem neuen Repo den Namen des Werkzeugs geben, es im Harness öffnen und sagen, was gebraucht wird. Der Agent erkennt den frischen Zustand, fragt Zweck und Owner und führt durch das Anforderungsgespräch – bis zum eingefrorenen, registrierten Werkzeug. Ein Repo pro Werkzeug, von Anfang an im eigenen Konto. Dieses Konzept-Repo muss dafür nie geöffnet werden.

**Der Weg im Harness:** Wer lieber ohne GitHub-Klick anfängt, öffnet dieses Repo oder installiert den Skill `skills/fachware` – dann legt der Agent das Werkzeug-Repo selbst an einem gewünschten Ort an. Beide Wege führen zum selben Werkzeug-Repo.

## Selbst ausprobieren

Dieses Repo ist die erste Instanz seiner eigenen Idee: Es erwartet, in einem Harness geöffnet zu werden.

```
Erkläre mir, was Fachware ist.
```

Oder direkt ein Werkzeug bauen:

```
Lass uns ein neues Fachwerkzeug bauen.
```

Der Agent klärt Name und Ablageort, legt das Werkzeug-Repo dort an und führt ohne Pause durch das Anforderungsgespräch – Repo-Handarbeit entfällt.

**Überall statt nur hier:** Der Skill lässt sich dauerhaft im Harness installieren – bitte den Agenten einfach darum. Er kopiert `skills/fachware` selbst an die richtige Stelle (bei Claude Code z. B. `~/.claude/skills/`). Danach funktioniert das Bauen in jedem Kontext, ohne dieses Repo.

## Status

Version 0.5.0 – Einzelheiten im [CHANGELOG](CHANGELOG.md). Erfahrungsberichte sind willkommen.

Die Zielgruppe sind wahrscheinlich derzeit Fachleute mit technischem Hintergrund. Jedenfalls solange Identität und Zugriff ungelöst sind, führt an API-Tokens kein Weg vorbei. Warum, steht im [Papier](paper/fachware.md) unter »Einordnung und Grenzen«.

## Lizenz und Zitieren

Code und Template: [MIT](LICENSE). Texte in `paper/` und `spec/`: [CC BY 4.0](LICENSE-docs) – Weiterverwendung mit Namensnennung. Zitierfähig über [CITATION.cff](CITATION.cff).
