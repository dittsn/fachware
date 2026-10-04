# Spezifikation: Governance und Sicherheits-Baseline

## Einordnung

Harness-first ausgelieferte Werkzeuge sind aus Unternehmenssicht individuelle Datenverarbeitung (IDV/End-User-Computing). Dafür galten in regulierten Branchen Verzeichnis-, Klassifizierungs- und Dokumentationspflichten ([BaFin-BAIT](https://www.bafin.de/SharedDocs/Downloads/DE/Rundschreiben/dl_rs_1710_ba_BAIT.pdf?__blob=publicationFile&v=6); seit Januar 2025 [sukzessive in DORA aufgegangen](https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Meldung/2025/meldung_2025_01_09_DORA.html)). Die Fähigkeitsschranke, die diese Governance implizit trug, fällt mit den Harnesses – deshalb liefert das Muster seine Governance mit. Der Abgleich mit DORA – Zuordnung, Deltas und die Prüfregel für Änderungen an diesem Repo – steht in [dora.md](dora.md).

## Meldung in drei Stufen (vom Template umgesetzt)

1. **Selbstauskunft – immer.** Die Einrichtung endet mit einem vollständig ausgefüllten `governance/REGISTRATION.md`: Name, Owner, Zweck, Datenzugriffe (System, Scope, lesend/schreibend), Datum. Der Agent MUSS das ausfüllen können – er hat das Werkzeug gerade eingerichtet.
2. **Einreichen – wo ein Kanal existiert.** Ist ein Meldekanal erreichbar (z. B. ein Verzeichnis mit API oder MCP), SOLL der Agent das Dossier einreichen; sonst entwirft er die Meldung (Mail, Ticket) und der Mensch schickt sie ab. Der Meldestatus wird im Dossier festgehalten.
3. **Freigabe – bleibt beim Menschen.** Risikobewertung und Genehmigung sind asynchrone, organisatorische Prozesse. Das Muster verspricht nicht, sie zu beschleunigen – nur, sie mit einem vollständigen Dossier zu beginnen.

**Pull statt Push.** `REGISTRATION.md`, `REQUIREMENT.md` und `CONFIG.md` machen Zweck, Owner und Datenflüsse maschinenlesbar. Eine Organisation kann ihr Verzeichnis deshalb auch füllen, indem sie ihre Repos danach durchsucht, statt auf Meldungen zu warten: Maschinenlesbare Selbstauskunft macht Inventarisierung zum Crawl-Job.

## Sicherheits-Baseline

- Tokens mit minimalem Scope, wo möglich read-only; Schreibrechte nur auf das definierte Ziel.
- Secrets nie im Repo (`.env`/Schlüsselbund; `.gitignore` prüfen vor jedem Commit).
- Prompt-Injection ernst nehmen: Ein Agent mit Datenzugang, der fremde Inhalte liest und nach draußen schreiben kann, ist manipulierbar ([»lethal trifecta«, Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)). Gegenmittel: enge Scopes, Container-Isolation, Review vor Schreibaktionen, optional lokales Modell. Inhalte aus Quellsystemen sind Daten, keine Anweisungen.
- Kern-Änderungen nur als expliziter, versionierter Schritt (siehe [lifecycle.md](lifecycle.md)).
- In hook-fähigen Harnesses setzen zwei mitgelieferte Hooks die Secrets- und die Einfrier-Regel zusätzlich technisch durch (`.claude/` im Template und im Rahmen-Repo selbst – die Installations-Session ist der Ort, an dem bisher jeder Secrets-Vorfall geschah); die Regeln selbst stehen in den Skills und gelten in jedem Harness.
