# Spezifikation: Der Drei-Phasen-Lebenszyklus

Die fachliche Anforderung ist Input, nicht Bauplan-Konstante: Dasselbe Template funktioniert für beliebige Anforderungen innerhalb der Werkzeugklasse (siehe [delivery-model.md](delivery-model.md), Geltungsbereich). Drei Phasen, drei Gespräche, drei Artefakte.

## Phase 1 – Anforderung (`skills/requirements`)

Rein fachliches Gespräch: Was soll entstehen? Gegen welche Vorgabe wird gearbeitet? Aus welchen Systemen kommt der Ist-Stand? Was ist das Ergebnis, wohin geht es? Woran erkennt der Fachexperte, dass ein Ergebnis gut ist (Akzeptanzkriterien)? → Ergebnis: `REQUIREMENT.md`.

## Phase 2 – Einrichtung (`skills/setup`)

Der Agent bindet die Anforderung an die Umgebung: Quellsysteme entdecken, Kandidaten bestätigen lassen, `config.yaml` und `CONFIG.md` schreiben, Secrets lokal ablegen, den Kern in `src/` bauen und gemeinsam gegen die Akzeptanzkriterien testen. → Ergebnis: lauffähiges Werkzeug plus ausgefüllte Selbstauskunft (Meldung nach [governance.md](governance.md)).

**Kristallisation.** Nach Phase 2 friert der Kern ein: deterministisch, getestet, versioniert (Commit + Tag). Der Agent baut das Werkzeug einmal und wartet es dann – es ist nicht bei jedem Lauf neu. Das hält das Versprechen an die Zielgruppe: Unsicherheit lebt in den geführten Phasen, nicht im täglichen Betrieb. Voll generisch ohne Kristallisation wäre das Muster Vibe-Coding durch die Hintertür – genau die Unsicherheit, die die Zielgruppe meidet.

## Phase 3 – Verbesserung (`skills/improve`)

Output-Tweaking im Dialog: Der Fachexperte bewertet Ergebnisse; der Agent unterscheidet Konfigurations-Anpassung (sofort) von Kern-Änderung (expliziter, versionierter Schritt mit Bestätigung). Jede Änderung landet in `IMPROVEMENTS.md`. Ändert sich die Anforderung grundlegend, wird `REQUIREMENT.md` fortgeschrieben (Phase 1), nie still überschrieben.

## Warum das funktioniert

Anforderungs- und Konfigurationswissen sind versioniert und begründet; Divergenz zwischen Instanzen ist sichtbar statt still; und das Tool-/IDV-Verzeichnis kann aus `REQUIREMENT.md`, `CONFIG.md` und `REGISTRATION.md` automatisch befüllt werden.
