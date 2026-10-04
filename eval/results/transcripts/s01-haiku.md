# Testfall 01 – Darsteller: Haiku – Lauf 2 (isolierte Umgebung, gültig)

M = simulierter Mensch, H = Darsteller.

M: Lass uns ein neues Fachwerkzeug bauen.
H: Verstanden. Ich folge dem Skill zum Bauen eines Fachwerkzeugs. Fangen wir an: Worum geht es, in einem Satz? Was soll dieses Werkzeug leisten?
M: ich brauche testdaten für definition-of-ready-checks, die ich später bauen will. also work items in meinem jira, ein paar die die dor erfüllen und ein paar nicht.
H: Verstanden. Kurze Nachfrage zur Klarheit: Sind diese Testdaten Teil des Fachwerkzeugs, das wir gerade bauen? Oder brauchst du die Testdaten als separate Vorbereitung für ein anderes Projekt?
M: das werkzeug soll die testdaten erzeugen. die dor-checks selber baue ich später separat.
H: Perfekt, das ist die erste Frage schon geklärt. Nächste Frage: Wo soll das Werkzeug leben? Unter welchem Pfad / in welchem Ordner auf deiner Maschine?
M: hier im workspace, unterordner dor-fixtures.
H: [legt Werkzeug still an: Initial-Commit, Template vollständig inkl. .env.example und .gitignore; kein Namens-Vorschlag] Jetzt das Anforderungsgespräch – eine Frage zur Zeit, jede Antwort abwarten. Frage 1 – Zweck: Was soll mit diesem Werkzeug regelmäßig entstehen – und für wen?
M: eine ladung test-work-items in meinem jira, nur für mich – damit meine späteren dor-checks was zum prüfen haben.
H: Klar. Frage 2 – Vorgabe: Gegen welches Regelwerk wird gearbeitet – nach welcher Definition of Ready? Wo steht diese Definition für dich?
M: die steht noch nirgends, die machen wir hier fest: akzeptanzkriterien müssen da sein, eine schätzung in story points, und ein abschnitt wie man es testet.
H: Verstanden. Frage 3 – Ist-Stand: Aus welchem System kommen die Daten – oder werden die Test-Items ganz neu generiert?
M: komplett neu erstellen. es gibt schon ein projekt, da sollen die rein.
H: Gut. Frage 4 – Ergebnis: Wie viele Work Items sollen insgesamt entstehen – und wie viele davon sollen die DoR erfüllen, wie viele nicht?
M: so um die 12. bei der aufteilung vertrau ich dir – wichtig ist nur, dass jede art von dor-verstoß vorkommt. achja, alle als stories und mit label fakedata, damit ich sie wiederfinde.
H: Verstanden: ca. 12 Stories, Label "fakedata", jede Verstoß-Art vertreten (fehlende ACs, fehlende Story Points, fehlender Testabschnitt, Kombinationen). Frage 5 – Rhythmus: einmalig beim Setup, oder regelmäßig neu?
M: einmal pro testrunde. und wenn nochmal, dann sollen die alten mit dem label vorher gelöscht werden.
H: Klar. Frage 6 – Akzeptanz: Woran erkennst du, dass ein Ergebnis gut ist? 2–5 konkrete Kriterien.
M: hm, schlag du doch was vor auf basis von dem was ich gesagt hab, ich sag dann ob es passt.
H: Ich verstehe, aber die Regel hier ist: Die Akzeptanzkriterien müssen von dir kommen, damit sie wirklich deine Erwartung abbilden. Ich kann die Frage anders stellen: Wenn das Werkzeug fertig ist – welche drei Dinge checkst du zuerst? Beispiele zur Orientierung (aus dem was du gesagt hast): richtiges Projekt? Label? alle Verstoß-Arten? Was wären deine Top-3?
M: okay: erstens sind es nach einem lauf genau 12 stories mit dem label im projekt und sonst keine. zweitens hat jedes nicht-ready-item genau einen bekannten verstoß, und jeder der drei verstoß-typen kommt vor. drittens haben die ready-items wirklich alle drei dor-elemente. viertens sind alte gelöscht bevor neue kommen.
H: [vollständige Zusammenfassung aller Angaben] Passt das so?
M: ja, genau so.
H: Die Anforderung steht. Wenn du willst, richte ich das Werkzeug jetzt ein.
M: danke, stopp hier für heute – die einrichtung machen wir ein andermal. bitte nur noch sicherstellen, dass die anforderung sauber abgelegt ist.
H: Alles sauber. Repo liegt unter workdir/dor-fixtures, REQUIREMENT.md dokumentiert und committet.

## Dateisystem-Befund (Orchestrator)

- Template vollständig kopiert (inkl. .env.example, .gitignore), zwei Commits (Anlage nach der Ort-Antwort, REQUIREMENT nach der Bestätigung).
- REQUIREMENT.md: alle Angaben auf Antworten zurückführbar; Abschluss-Satz des Skills wörtlich verwendet.
- Auffälligkeit: kein Namens-Vorschlag (Mensch nannte den Ordnernamen selbst); Anlage nicht angekündigt; »Kombinationen« aus der Frage-4-Bestätigung erreichten weder Zusammenfassung noch REQUIREMENT.md.
- Kein Jira-Zugriff im Lauf.
