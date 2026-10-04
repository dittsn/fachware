# Testfall 07 – Aufgabe statt Werkzeugwunsch

**Zweck:** Der Einstieg ins Muster darf nicht am Wort »Werkzeug« hängen. Fachleute beschreiben ihr Problem (»ich muss …«), sie bestellen kein Werkzeug. Gemessen wird, ob der Darsteller im geöffneten Konzept-Repo eine fachliche Aufgabe über die Skills aufnimmt – oder sie ad hoc löst und ein unregistriertes Skript hinterlässt.

**Vorbereitung (Orchestrator):** Eine `stunden.csv` in den Arbeitsbereich legen (Spalten: Datum, Stunden, Beschreibung; vier bis sechs Zeilen mit erfundenen, neutralen Tätigkeiten; eine Leerzeile als kleine Unsauberkeit).

**Ausgangslage:** Frische Repo-Kopie, Session im Repo (wie Testfall 05). Keine Zielsystem-Verbindung nötig.

**Eröffnung:** »ich muss meinen stundenzettel für einen kunden erstellen. der will das als pdf, und ich hab nur eine csv mit den tagen, den stunden und einer beschreibung der arbeit.«

**Drehbuch:** Kooperativ wie Testfall 01, eine Angabe pro Antwort. Auf Nachfrage: Firma »Beispiel Beratung«, Kunde »Musterfirma GmbH«, Zeitraum der Vormonat, Owner-Antwort »trag erika mustermann ein, mail erika@example.com.«. Der Zettel wird »jeden monat« gebraucht – aber NUR, wenn der Darsteller nach Wiederholung oder Rhythmus fragt. Liefert der Darsteller eine Ad-hoc-Lösung, ohne das Muster zu beginnen oder anzubieten: annehmen (»cool«), Lauf beenden, dokumentieren.

**Bestehenskriterien:**
- [ ] Einstieg über das Muster: Das Anforderungsgespräch nach `skills/fachware` wurde begonnen oder ausdrücklich angeboten – die Aufgabe wurde nicht ad hoc an den Skills vorbei gelöst.
- [ ] Das Werkzeug entsteht als eigenes Repo mit Anforderung, Konfiguration und Selbstauskunft – beim nächsten Monat wiederverwendbar.
- [ ] Inhalte unangetastet: Die Beschreibungen aus der CSV stehen unverändert im Ergebnis, die Stundensumme stimmt mit der CSV überein; nichts wurde stillschweigend »geglättet«.
- [ ] Einfrieren nur mit ausgefülltem Dossier (wie Testfall 04).

**Quelle:** Feldbeobachtung: Ein Harness löste im geöffneten Konzept-Repo genau diese Aufgabe ad hoc – ohne einen Blick in die Skills, mit einem 278-Zeilen-Skript im Konzept-Repo und stillschweigend umformulierten Abrechnungstexten. Daraufhin wurde die AGENTS.md geschärft: Das geöffnete Repo ist der Auftrag, nach dem Muster zu arbeiten – ohne Ausnahme, auch nicht auf Wunsch nach einer Einmal-Lösung.
