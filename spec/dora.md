# Spezifikation: DORA-Abgleich

## Zweck und Geltung

Die Verordnung (EU) 2022/2554 (DORA) bindet Finanzunternehmen und löst dort die BAIT ab; sie ist der strengste Rahmen, in dem dieses Muster laufen können muss. Diese Datei verbindet das Muster mit DORA, ohne die Governance des Musters daran zu koppeln: Die Regeln in [governance.md](governance.md) gelten aus eigenem Recht und für alle Nutzer. Hier steht, welche Eigenschaft des Musters welche DORA-Anforderung bedient, welche Lücken bleiben und wie Änderungen an diesem Repo geprüft werden. Diese Datei ist keine Rechtsberatung.

## Zuordnung

| Eigenschaft des Musters | DORA | Status |
| --- | --- | --- |
| Selbstauskunft (`governance/REGISTRATION.md`) nennt Zweck, angebundene Systeme und Datenzugriffe vollständig und maschinenlesbar; »Pull statt Push« | Artikel 8 (Identifizierung, Inventar) | erfüllt |
| Owner ist eine für Dritte erreichbare Person oder Rolle mit Kontaktweg; Personen-Angaben stammen ausschließlich aus Antworten des Menschen | Artikel 5 und 8 (Verantwortlichkeit) | erfüllt |
| Dossier nennt Harness, Modell und Anbieter (bei Cloud-Modellen mit dem Hinweis, dass gelesene Inhalte dorthin abfließen) sowie die Art des Datenzugriffs | Artikel 28 (Drittparteirisiko, Informationsregister) | teilweise – siehe Deltas |
| Tokens mit kleinstem Scope, lesend vor schreibend; Secrets nie im Repo und nie im Gespräch, Dateien mit Secrets werden über ihre Struktur geprüft | Artikel 9 (Schutz und Prävention) | erfüllt |
| Kern-Änderungen nur als expliziter, versionierter Schritt über Phase 3; der Tag setzt die Bestätigung des Menschen und das ausgefüllte Dossier voraus | Artikel 9 (Änderungssteuerung) | erfüllt |
| Eingefroren wird nur, was gegen die Akzeptanzkriterien am Zielsystem geprüft wurde | Artikel 24 folgende (Tests, sinngemäß) | erfüllt |
| Das Dossier wird bei Änderungen nachgeführt; was der Mensch nicht weiß, wird ausdrücklich als unbekannt eingetragen und nicht weggelassen (etwa der Token-Ablauf) | Artikel 8 und 28 (Aktualität) | erfüllt |
| Fehlschläge, Nebenwirkungen und Vorfälle werden dem Menschen offengelegt statt als Erfolg gemeldet; Meldung in drei Stufen | Artikel 17 folgende (Vorfallsmeldung, sinngemäß) | teilweise – siehe Deltas |

## Deltas für den Einsatz im Finanzkontext

Das Template baut nicht alles ein, was DORA von einem Finanzunternehmen verlangt. Wer das Muster dort einsetzt, muss zusätzlich lösen:

- **Kritikalitäts-Einstufung.** Das Dossier hat kein Pflichtfeld »kritisch / nicht kritisch«. Die Einstufung gehört der Organisation; im Finanzkontext ist sie im Dossier zu ergänzen.
- **Registerformat.** Das Informationsregister ist nach der ESA-Vorlage maschinenlesbar einzureichen. Das Dossier liefert die Angaben, nicht das Einreichformat.
- **Meldefristen.** Fristen und Schwellenwerte der Vorfallsmeldung richten sich an das Unternehmen. Das Werkzeug liefert die ehrliche Selbstauskunft als Zulieferung, keinen Meldeprozess.
- **Registeranschluss.** Der Anschluss an ein Verzeichnis ist ein Adapter je Organisation, kein Versprechen des Templates. Register werden unterschiedlich geführt: als Excel nach der ESA-Vorlage, in GRC-Plattformen, in EAM-Werkzeugen wie LeanIX oder Alfabet, in End-User-Computing-Verzeichnissen. Ein Crawler, der Repos durchsucht und die Dossier-Felder in das jeweilige Ziel schreibt, lässt sich selbst als Fachwerkzeug nach diesem Muster bauen. Für das DORA-Register existiert mit der ESA-Vorlage ein kanonisches Zielformat, gegen das sich die Zuordnung der Felder konkret definieren lässt.

## Prüfregel für Änderungen an diesem Repo

Vor jedem Einbau wird gefragt: Berührt die Änderung eine Eigenschaft aus der Zuordnungstabelle? Wenn nein, ist nichts zu vermerken. Wenn ja: Stärkt oder hält sie die Eigenschaft, genügt ein Satz im Commit oder im Protokoll der Testsuite. Schwächt sie die Eigenschaft, wird das vor dem Einbau benannt und entschieden. Neue DORA-Anforderungen kommen nur durch bewusste Entscheidung in die Tabelle; die Prüfregel zieht das Muster nicht von selbst auf den vollen Umfang der Verordnung.
