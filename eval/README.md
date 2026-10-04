# Eval-Suite: Installations-Gespräche wiederholbar testen

Die Feldtests haben gezeigt, wo Installations-Gespräche scheitern. Diese Suite macht die Befunde wiederholbar: Jeder Testfall ist ein Drehbuch für ein simuliertes Installations-Gespräch plus harte Bestehenskriterien. Die Suite prüft zweierlei: ob die Logik der Skills funktioniert, und – bei Läufen desselben Testfalls mit verschiedenen Modellstufen – wo die Gesprächsregeln je Modell halten. Portabilität auf fremde, schwache Modelle prüft sie nicht; dafür bleiben echte Feldtests die Quelle.

## Drei Rollen

- **Werkzeug-Harness (Darsteller):** Ein Agent, der nichts bekommt als eine Kopie dieses Repos und die Eröffnungsnachricht aus dem Testfall. Er kennt weder Drehbuch noch Bestehenskriterien.
- **Simulierter Fachexperte:** Führt das Gespräch nach dem Drehbuch. Regeln ohne Ausnahme: antwortet nur auf Gestelltes, liefert nie unaufgefordert Informationen, eine Angabe pro Antwort, hält sich an die vorgegebenen Formulierungen – auch die unkooperativen.
- **Prüfer (`pruefung.py`):** Entscheidet die mechanisch nachprüfbaren Kriterien deterministisch aus Request-Log, Git-Historie, Transkript und Serverzustand – gleiche Eingaben, gleiche Befunde, jeweils mit Fundstelle. Hier urteilt kein Modell.
- **Bewerter:** Bekommt das vollständige Transkript, die Prüfer-Befunde und die verbleibenden auslegungsbedürftigen Kriterien, sonst nichts. Jedes Kriterium wird einzeln mit PASS/FAIL bewertet; ein FAIL zählt nur mit wörtlichem Zitat als Beleg. Kein Gesamturteil ohne Einzelbewertung. Der Bewerter ist selbst ein Modell und streut wie eines – deshalb entscheidet er so wenig wie möglich, und Nachfragen der Art »bist du sicher?« sind kein Prüfmittel: Darauf kippen Urteile unabhängig von der Sache.

## Ablauf

Automatisiert führt ihn der Skill `skills/eval/SKILL.md` aus (fragt vorab nach Testfällen und Darsteller-Modellen); die Schritte im Einzelnen:

1. Frische Repo-Kopie für den Darsteller, Testfall auswählen.
2. Gespräch führen, bis der Testfall sein definiertes Ende erreicht (oder der Darsteller aufgibt).
3. Bewertung; Ergebnis als Datei nach `eval/results/` (`testfall-NN-<lauf>.md`): Modell des Darstellers, Kriterien mit PASS/FAIL und Fundstellen, Auffälligkeiten außerhalb der Kriterien.
4. Jeder FAIL führt zu genau einer Frage: Fehlt eine Regel im Skill, oder hält das Modell die Regel nicht ein? Nur im ersten Fall wird der Skill geändert – dann Testfall erneut fahren.

## Grenzen

Ein simulierter Mensch produziert keine echten Überraschungen; neue Testfälle entstehen aus Feldtests, nicht am Schreibtisch. Und ein PASS mit einem starken Modell sagt nichts über schwache Modelle – der Kalibrierungs-Befund aus dem Papier (Regeln einhalten und das eigene Handeln zurückhalten wandern nicht mit der Modellstufe) gilt auch hier.

Die private Konto-Mailadresse des Testbetreibers ist in allen Transkripten und Auswertungen zu `<Konto-Mail>` redigiert. Die Identitätsleck-Befunde (Modelle übernahmen die Konto-Identität in Commits) beziehen sich auf diese Adresse; für den Befund zählt, dass es die echte Konto-Adresse war, nicht ihr Wortlaut.

Seit Version 0.5.0 ist der Standardweg für Nutzer das Template-Repo `dittsn/fachware-template`. Die Testfälle beschreiben bisher den Weg über das geöffnete Konzept-Repo beziehungsweise den installierten Skill; ein Testfall gegen den Template-Weg (frisch erzeugtes Repo, Erkennung des frischen Zustands) steht aus.
