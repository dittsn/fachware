# Spezifikation: Das Auslieferungsmodell

Normative Kurzfassung des Musters. Schlüsselwörter MUSS/SOLL/KANN sinngemäß nach RFC 2119.

## Geltungsbereich

Fachware ist für Werkzeuge gedacht, die teamintern oder persönlich sind, batchartig arbeiten, ausschließlich über APIs mit den Fachsystemen sprechen, außer ihrer Konfiguration keinen eigenen (Mehrbenutzer-)Zustand halten und keine Always-on-Pflicht haben. Für Systems of Record, Echtzeit-Kollaboration oder Always-on-Dienste ist das Muster ausdrücklich nicht gedacht.

## Anforderungen

1. **Distribution.** Ein Werkzeug MUSS als Git-Repository ausgeliefert werden. Sign-up, Deployment oder Server-Betrieb DÜRFEN NICHT Voraussetzung sein. Ein Werkzeug SOLL aus einer Vorlage entstehen, die selbst ein Repo ist (Referenz: `dittsn/fachware-template`, als GitHub-Template) – ein Repo je Werkzeug, von Anfang an im Konto des Owners; die Anlage durch einen installierten Skill ist der gleichwertige zweite Weg.
2. **Maschinenlesbare Absicht.** Das Repo MUSS ein AGENTS.md enthalten, das einem Harness sagt, was das Werkzeug ist und wie Einrichtung und Betrieb ablaufen. Skills (SKILL.md) SOLLEN die Gespräche der Lebenszyklusphasen führen (siehe [lifecycle.md](lifecycle.md)).
3. **Installation als Fachgespräch.** Die Einrichtung MUSS ohne Konfigurationsanleitung möglich sein: Der Agent fragt fachlich, schaut in den Quellsystemen nach, schlägt Kandidaten vor und schreibt die Konfiguration selbst. Technische Begriffe SOLLEN nur auftauchen, wo sie unvermeidbar sind (z. B. Token-Erzeugung). Der Agent DARF fachliche Inhalte NICHT erfinden: Jede Angabe in Anforderung und Konfiguration stammt aus einer bestätigten Antwort des Menschen, und die Verbindung zu den Zielsystemen wird geklärt, bevor gebaut wird.
4. **Lokale Vertrauensgrenze.** Secrets MÜSSEN auf der Maschine bleiben (`.env`/Schlüsselbund, per `.gitignore` ausgeschlossen) und DÜRFEN NIE in das Repository gelangen. Der Betrieb mit lokalem Modell KANN unterstützt werden und DARF NICHT durch die Bauform verhindert werden.
5. **Konfiguration als Dialog.** Anpassungen MÜSSEN im Gespräch möglich sein. Die Konfiguration MUSS lesbar und begründet abgelegt werden (`config.yaml` + `CONFIG.md`).
6. **Harness-Portabilität.** Das Repo SOLL sich auf offene Formate stützen (AGENTS.md, SKILL.md, MCP) statt auf herstellerspezifische, damit Copilot, Claude, pi und andere dasselbe Repo bedienen können.
7. **Governance.** Die Einrichtung MUSS mit einer vollständig ausgefüllten Selbstauskunft enden; Einreichen und Freigabe folgen dem Drei-Stufen-Modell in [governance.md](governance.md).
