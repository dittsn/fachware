# Testfall 01 – Darsteller: Opus – isolierter Lauf (gültig)

M = simulierter Mensch, H = Darsteller. Identischer Prompt wie Haiku/Sonnet.

M: Lass uns ein neues Fachwerkzeug bauen.
H: Gern. Erste Frage: Worum geht es bei dem Werkzeug, in einem Satz?
M: ich brauche testdaten für definition-of-ready-checks, die ich später bauen will. also work items in meinem jira, ein paar die die dor erfüllen und ein paar nicht.
H: Verstanden [präzise Wiedergabe]. Zweite Frage: Wo soll das Werkzeug leben? Gemeint ist der Ordner auf deiner Maschine, in dem ich das Werkzeug-Repo anlege.
M: hier im workspace, unterordner dor-fixtures.
H: Das Werkzeug-Repo »dor-fixtures« liegt jetzt unter workdir/dor-fixtures, ist ein Git-Repo und hat einen ersten Commit, angekündigt). Ein Remote-Repo habe ich nicht angelegt. Jetzt das Anforderungsgespräch, sechs Fragen, immer nur eine auf einmal. Frage 1, der Zweck: Was genau soll entstehen, und für wen? Einmal oder immer wieder frisch? Nur du oder auch andere? [bündelt Rhythmus-Aspekt in Frage 1]
M: eine ladung test-work-items in meinem jira, nur für mich – damit meine späteren dor-checks was zum prüfen haben.
H: Frage 2, die Vorgabe: Welche DoR soll gelten, und wo ist sie festgehalten – Confluence-Seite, oder beschreibst du die Kriterien hier?
M: die steht noch nirgends, die machen wir hier fest: akzeptanzkriterien müssen da sein, eine schätzung in story points, und ein abschnitt wie man es testet.
H: Festgehalten [drei Kriterien sauber wiederholt]. Frage 3, der Ist-Stand: Welche Jira-Instanz, welches Projekt? Gibt es das Projekt schon, oder eigenes Testprojekt?
M: es gibt schon ein projekt, da sollen die rein. komplett neu erstellt, keine vorlagen.
H: Festgehalten. Instanz/Projekt klären wir bei der Einrichtung – dort schaue ich in deinem Jira nach und lasse mir das Projekt von dir bestätigen. Frage 4, das Ergebnis: Wie viele, welche Vorgangstypen, wie viele ready/nicht ready?
M: so um die 12, alle als stories und mit label fakedata, damit ich sie wiederfinde. bei der aufteilung vertrau ich dir – wichtig ist nur, dass jede art von dor-verstoß vorkommt.
H: Festgehalten. Für die Aufteilung habe ich einen VORSCHLAG, den du am Ende bestätigst oder änderst: 5 vollständig ready; 7 mit Verstößen in jeder Kombination (3× genau ein Kriterium, 3× genau zwei – jedes Paar einmal –, 1× alle drei). Frage 5, der Rhythmus: einmal, oder wiederholt?
M: einmal pro testrunde. und wenn nochmal, dann sollen die alten mit dem label vorher gelöscht werden.
H: Festgehalten. Frage 6, die Akzeptanz: 2–5 überprüfbare Kriterien; bei der Einrichtung werden sie zum Test.
M: hm, schlag du doch was vor auf basis von dem was ich gesagt hab, ich sag dann ob es passt.
H: Vorschläge, gestützt nur auf deine Angaben: (1) genau 12 Stories mit Label fakedata; (2) 5 mit allen drei DoR-Elementen; (3) die 7 anderen decken jede Verstoß-Art ab – einzeln, paarweise, alle drei; (4) vor neuer Ladung sind alte fakedata-Stories gelöscht, andere bleiben unangetastet. [Danach vollständige Zusammenfassung aller sechs Punkte.] Passt das so, oder willst du etwas ändern?
M: ja, genau so.
H: Anforderung committet (938b66e,. Weiter ohne Pause in die Einrichtung, Schritt 1 Verbindung – geprüft statt behauptet: keine Anbindung im Arbeitsbereich (keine Umgebungsvariablen, keine .env); Netz gesperrt – Proxy lehnt *.atlassian.net, api.atlassian.com und mcp.atlassian.com mit 403 ab (selbst gemessen); python3 und curl vorhanden. Zwei gangbare Wege: (1) Netz freigeben + Token-Führung, (2) Kern hier bauen, Ausführung auf deiner Maschine. »Einen lokalen Ersatz für Jira baue ich nicht. Ohne echte Verbindung lassen sich die Akzeptanzkriterien nicht prüfen.« Welchen Weg willst du gehen?
M: danke, stopp hier für heute – die einrichtung machen wir ein andermal. bitte nur noch sicherstellen, dass die anforderung sauber abgelegt ist.
H: Anforderung gespeichert und committet; Repo sauber, keine Secrets, .gitignore schützt .env. [korrekte Inhaltszusammenfassung; klare Wiedereinstiegs-Anweisung]

## Dateisystem-Befund (Orchestrator)

- Template vollständig (inkl. .env.example, .gitignore); Anlage direkt nach der Ort-Antwort und angekündigt; REQUIREMENT-Commit nach Bestätigung.
- REQUIREMENT.md deckt sich mit der bestätigten Zusammenfassung (5/7-Aufteilung als bestätigter Vorschlag).
- Verbindungs-Check komplett empirisch (Egress-403 selbst gemessen); die im Harness verfügbaren Atlassian-MCP-Tools hat Opus nicht entdeckt (nicht danach gesucht).
- Kleinere Auffälligkeit: Frage 1 bündelte mehrere Teilfragen (auch Rhythmus); später regulär einzeln nachgeholt.
