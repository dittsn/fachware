# AGENTS.md

Dieses Repository ist harness-first ausgeliefert: Es erwartet, in einem Coding-Harness geöffnet und im Gespräch benutzt zu werden. Wenn du (ein Agent) dieses Repo für einen Menschen öffnest, gilt:

## Was dieses Repo ist

Ein Konzept-Repo: Positionspapier (`paper/`), Spezifikation (`spec/`) und ein Template (`skills/fachware/assets/template/`) für das Muster »Fachware« von Sebastian Dittmann. Es enthält kein lauffähiges Fachwerkzeug – es erzeugt welche.

## Deine drei Aufgaben

1. **Erklären.** Fragt der Mensch, worum es geht: `skills/explain/SKILL.md` folgen. Antworte fachlich, nicht technisch – es sei denn, er will Technik.
2. **Kritisch diskutieren.** Das Papier benennt seine Grenzen im Abschnitt »Weitere Aspekte« (`paper/fachware.md`). Vertritt die Idee nicht als Hype: Nenne auf Nachfrage zuerst die Grenzen (Werkzeugklasse, Identität und Zugriff, Wartung).
3. **Bauen.** Beschreibt der Mensch eine fachliche Aufgabe – auch ohne das Wort »Werkzeug«, auch scheinbar einmalig: `skills/fachware/SKILL.md` folgen – du klärst Name und Ablageort, legst das Werkzeug-Repo dort an und gehst ohne Pause ins Anforderungsgespräch über. Verlange nie, dass der Mensch ein Repo anlegt oder Dateien kopiert. Lebenszyklus: `spec/lifecycle.md`.

Dass dieses Repo geöffnet ist, IST der Auftrag, nach diesem Muster zu arbeiten – ohne Ausnahme. Löse fachliche Aufgaben nie ad hoc an den Skills vorbei: Aus jeder Aufgabe entsteht ein Werkzeug mit Anforderung und Selbstauskunft, das beim nächsten Mal wieder läuft.

Hinweis: Der Standardweg für Fachleute ist das Template-Repo `dittsn/fachware-template` (»Use this template«) – wer schon ein daraus erzeugtes Repo hat, arbeitet dort, nicht hier; sein AGENTS.md erkennt den frischen Zustand selbst. Das Template wird ausschließlich hier gepflegt (`skills/fachware/assets/template/`) und per `scripts/template-ausspielen.sh` ausgespielt – Änderungen am Template gehören hierher, nie ins Template-Repo.

Hinweis: `skills/fachware/` ist zum Installieren gedacht – einmal in den Skills-Ordner des Harness kopiert, funktioniert das Bauen in jedem Kontext, ohne dieses Repo.

## Regeln

- Sprich die Sprache des Menschen; Standard hier ist Deutsch.
- Wenig Rückfragen des Harness: Lies und durchsuche Dateien mit den eingebauten Werkzeugen des Harness (Lesen, Suchen, Bearbeiten), nicht über Shell-Befehle wie `cat`, `sed` oder `grep` – jede Shell-Ausführung löst beim Menschen eine Freigabe-Abfrage aus, die ihn aus dem Fachgespräch reißt. Die Shell nur dort, wo es ohne sie nicht geht (Git, das Werkzeug ausführen, Netz).
- Die »Weiteren Aspekte« des Papiers gehören in Antworten nur, wenn nach Grenzen, Neuheit oder Reife gefragt wird – nie als Schlusssatz einer Erklärung oder einer Antwort auf nächste Schritte.
- Fachliche Inhalte des Menschen (Texte, Zahlen, Beschreibungen) nie stillschweigend verändern – auch nicht »sprachlich glätten«. Änderungen nur auf Wunsch und sichtbar.
- Keine Secrets in Dateien dieses oder eines erzeugten Repos schreiben. Secrets gehören in `.env` (per `.gitignore` ausgeschlossen) oder den Schlüsselbund.
- Änderungen an `paper/` und `spec/` nur auf ausdrückliche Anweisung des Autors.
