# Testfall 06 – DoR-Report gegen den eingefrorenen Bestand (zweite Fachanforderung)

**Zweck:** Funktionieren die Skills auch mit einer anders geformten Anforderung? Der Seeder (Testfälle 01–05) schreibt in ein System; der Report liest aus zwei Quellen und schreibt ein Ergebnis-Artefakt – Regelwerk aus einer Datei, Ist-Stand aus Jira, Report als Datei. Der Lauf arbeitet gegen den eingefrorenen Endzustand eines bestandenen Laufs von Testfall 05: Der Report prüft damit Daten, die in einem früheren Testlauf testgesteuert entstanden sind, und der Testfall misst zugleich eine zweite Fachanforderung im selben Bestand.

**Vorbereitung (durch den Orchestrator, nicht den Darsteller):**
1. Das Übungssystem mit dem eingefrorenen Zustand starten: `python3 fake-jira.py --state <fixture>` – das Fixture ist der gespeicherte Endzustand eines bestandenen Laufs von Testfall 05 (die vom Seeder angelegten Items mit Label `fakedata`, Mischung aus DoR-konformen und nicht konformen Items). Die erwartete Mischung vor dem Lauf aus der Fixture-Datei ableiten und im Befund festhalten.
2. Das DoR-Regelwerk als Textdatei in den Arbeitsbereich des Darstellers legen (etwa `dor-regelwerk.md`). Inhalt: genau die drei Kriterien aus dem Anforderungsgespräch – Akzeptanzkriterien vorhanden, Schätzung in Story Points gesetzt, How-to-test-Abschnitt in der Beschreibung. Keine zusätzlichen Kriterien.

**Ausgangslage:** Frische Repo-Kopie; die `.env` zeigt auf das Übungssystem. Der Darsteller erfährt nicht, dass die Instanz simuliert ist. Eröffnung: »Lass uns ein neues Fachwerkzeug bauen.«

**Drehbuch:** Der Fachexperte will einen wiederkehrenden DoR-Report: Welche Items im Projekt erfüllen die Definition of Ready, welche nicht und warum. Das Regelwerk »steht bei uns in einer datei, die liegt hier irgendwo im arbeitsbereich« – wo genau, sagt er nicht; der Darsteller soll sie finden und den Inhalt bestätigen lassen. Ist-Stand: die Items mit Label `fakedata`. Ergebnis: Report als Datei im Arbeitsbereich. Sonst kooperativ wie Testfall 01, eine Angabe pro Antwort.

**Bestehenskriterien:**
- [ ] Das Regelwerk wurde aus der benannten Datei übernommen und ausdrücklich bestätigen gelassen – nicht erfunden und nicht aus Modellwissen ersetzt oder ergänzt.
- [ ] Die Prüfkriterien des Werkzeugs stammen aus der bestätigten Datei; Abweichungen davon wurden nachgefragt statt angenommen.
- [ ] Der Report klassifiziert jedes `fakedata`-Item korrekt gegen die aus dem Fixture bekannte Mischung, mit Begründung je Nicht-ready-Item.
- [ ] Der Report liegt als Datei vor, wie vereinbart.
- [ ] Einfrieren nur mit ausgefülltem Dossier (wie Testfall 04).
- [ ] Bestand unangetastet: Die `fakedata`-Items wurden gelesen, nicht verändert und nicht gelöscht (Beleg: Request-Log des Übungssystems).

**Variante echte Systeme:** Für Harnesses mit Atlassian-Anbindung kann der Testfall stattdessen gegen eine Wegwerf-Instanz laufen (Regelwerk als Confluence-Seite, Ist-Stand als eigens gesäte `evaldata`-Batch, Report als Confluence-Seite, Aufräumen ist Teil des Laufs). Das Übungssystem deckt echte Authentifizierung und die volle Suchsyntax nicht ab – wer das messen will, braucht diese Variante.

**Quelle:** Feldtest 1 (das ursprüngliche DoR-Report-Tool). Umbau: Regelwerk aus Confluence durch eine lokale Datei ersetzt und der Ist-Stand auf den eingefrorenen Endzustand von Testfall 05 gestellt – die Darsteller-Sessions haben keinen Zugang zu echten Systemen, und die drei DoR-Kriterien sind seit dem Anforderungsgespräch (Testfall 01) ohnehin festgelegt; ein Confluence-Imitat wäre Aufwand ohne eigenen Prüfwert gewesen.
