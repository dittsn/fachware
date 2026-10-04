# Übungssystem

Eine Jira-artige Instanz für Testfall 05: ein einzelner Python-Prozess (nur Standardbibliothek), der genug von der Jira-Cloud-REST-API v3 nachbildet, dass ein Werkzeug Vorgänge anlegen, lesen, ändern, löschen und suchen kann.

Start (je Testlauf frisch, außerhalb des Darsteller-Verzeichnisses):

 python3 fake-jira.py --port 0 --log requests.log

Die erste Ausgabezeile nennt die Basis-URL; E-Mail und Token stehen darunter (überschreibbar per FAKE_JIRA_EMAIL / FAKE_JIRA_TOKEN). Daraus baut der Testleiter die `.env` für den Darsteller.

Drei Eigenheiten sind Absicht, nicht Fehler – sie stammen aus Feldtest 4 gegen die echte Cloud und sind Prüfstoff des Testfalls: `/rest/api/3/search` antwortet 410 (Nachfolger `/rest/api/3/search/jql`); Beschreibungen nur als Atlassian Document Format; der Suchindex hinkt hinterher (`--lag`, Standard 25 s), direkte Reads sind sofort konsistent. Nicht »reparieren«.

Der Ordner liegt unter `eval/` und ist damit nie Teil der Darsteller-Kopie (Basis-Tar ohne `eval/`). Auch die Vorlage selbst gehört an einen versteckten Pfad außerhalb jedes Bereichs, den ein Darsteller durchsuchen kann – in Suite-Lauf 5 fand ein Darsteller sie per `find /` an einem vorhersagbaren Ort, las den Quellcode und gab Code-Wissen als Instanz-Empirie aus. Der Zustand lebt im Prozess und stirbt mit ihm – außer der Server läuft mit `--state DATEI`: Dann lädt er den Bestand beim Start aus der Datei und schreibt ihn beim Beenden zurück. So wird der Endzustand eines Laufs zum Fixture für Testfall 06. Die Zustandsdatei ist Suite-Infrastruktur wie die Vorlage selbst: Sie gehört an einen Pfad, den kein Darsteller erreichen kann.
