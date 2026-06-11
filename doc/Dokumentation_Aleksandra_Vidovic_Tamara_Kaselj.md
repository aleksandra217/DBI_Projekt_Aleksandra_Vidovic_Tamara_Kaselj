# **NeuroCards**

## Projektgruppe: Aleksandra Vidovic & Tamara Kaselj
## Klasse: 3AHIF
## Jahr: 2026

# Link Repository: NICHT VERGESSEN!






## Betreuer: David Bechtold, Christoph Bauer                                                                                  
## Kurzbeschreibung: WIr erstellen ein Programm, wo man einen Ordner erstellen kann und dadrinnen kann man Karteikarten (offene Fragen, Multiple Choice, True/False) erstellen. Daraus lässt sich dann ein Quiz erstellen und dann sieht man eine Statistik, wo man auch sieht, wie viele Fragen man richtig und wie viele Fragen man falsch hatte.  


Collage mit mindestens zwei Screenshots 



1	Inhaltsverzeichnis







2	Projektzeitplan
|    Datum    |   Aufgabe  | Bearbeiter | Status (%) |
| ----------- | ---------- | ---------- | ---------- |
|  28.05.2026 | Beginn den Users in der FASTAPI aufzubauen | Aleksandra Vidovic | 70% |
|  31.05.2026 | Users in der FASTAPI fertig programmiert, Fehler waren vorhanden | Aleksandra Vidovic | 100 % | 
|  01.06.2026 | Fehler beim Users wurden behoben | Aleksandra Vidovic | 100 % |
|  01.06.2026 | Ordner in der FASTAPI programmieren | Aleksandra Vidovic | 70 % |
|  02.06.2026 | Ordner wurde in der FASTAPI fertig programmiert | Aleksandra Vidovic | 100 % | 
|  03.06.2026 | Karteikarten wurden in der FASTAPI programmiert | Aleksandra Vidovic | 100 % |
|  03.06.2026 | Code von allen model.py in eine model.py hinzugefügt | Aleksandra Vidovic | 100 % | 
|  08.06.2026 | Quiz wurde erstellt | Aleksandra Vidovic | 100 % | 
|  08.06.2026 | Statistik wurde erstellt | Aleksandra Vidovic | 50 % |
|  10.06.2026 | Bei der Statistik erhält man eine Ausgabe. Fehler wurde behoben | Aleksandra Vidovic | 90 % |
|  11.06.2026 | Fehler bei Users POST-Login gelöst | Aleksandra Vidovic | 100 % |
|  11.06.2026 | Fehler bei GET und POST von Ordner gelöst | Aleksandra Vidovic | 100 % |
|  11.06.2026 | Fehler beim zweiten GET - ordnerid gelöst, somit hat auch dann PUT getan | Aleksandra Vidovic | 100 % |
|  11.06.2026 | Fehler bei Karteikarten gelöst, außer beim ersten GET, wo man alle Karteikarten erhaltet | Aleksandra Vidovic | 80 % |
|  11.06.2026 | Fehler bei Quiz bei POST, GET, GET id und DELETE gelöst. Zwei müssen noch gelöst werden. | Aleksandra Vidovic | 60 % |
|  11.06.2026 | Fehler bei Statistik gelöst | Aleksandra Vidovic | 100 % |










3	Lastenheft (Kurzbeschreibung, Funktionsumfang, Skizzen)
2.1. Kurzbeschreibung  
## verändern?? 
Spielprinzip mit einigen Sätzen erklären
Wenn man keinen Account hat, dann muss man sich zuerst registriernen und ansonsten anmelden. Dann gelangt man in das Hauptfenster des Benutzers wo man einen Ordner erstellen kann, draufklicken kann und dann Karteikarten (offene Fragen, Multiple Choice, True/False) erstellen kann. Daraus kann man dann quizze machen und bekommt eine Statistik, wie viele Fragen man richtig hatte und wie viele Fragen man falsch hatte.  

2.2. Skizzen
### fehlen hier noch
2.3. Funktionsumfang
## notieren 
Alle Funktionen genau erklären.
## noch machen.
Must-Haves und Nice-To-Haves beschreiben (Punkteliste). Must-Haves müssen umgesetzt werden.
Must-Haves:
- Mehrere Ordner können erstellt werden.
- Mehrere Karteikarten können erstellt werden.
- Quizze können erstellt werden, gestartet werden und gemacht werden.
- Der User kann sich anmelden -> Login 
- Der User muss sich zuerst registrieren, wenn er noch keinen Account hat. 
- Statistik: Das System speichert immer nach jedem Quiz ab, wie viele Richtige und Falsche Antworten man hatte und auch das Datum -> Aktualisierung. 

Nice-Haves:
- Bei dem Ordner eine Farbe auswählen können. 
- Limit bei Karteikarten setzen. 
- Limit bei Erstellung von Quizzes erstellen. 
Beispiele: 
## vielleicht? 
Taste D	Bewegt die Spielerfigur um 5 Pixel nach rechts
Taste S	Speichert aktuellen Zustand des Spiels (Save)
Mausklick	Zerstört Sprite unter dem Cursor
	


 
4	Pflichtenheft 
4.1	Interner Programmaufbau (Programmlogik)
Klassendiagramme, um die Klassen abzubilden.
Wie arbeiten die Klassen miteinander? Hier könnt ihr beispielsweise Flussdiagramme verwenden, um dies abzubilden.
4.2	Umsetzungsdetails
Detaillierte Beschreibung der Umsetzung mit möglichen Fehlern und Lösungen
## noch machen. 
|    Datum    |   Fehler   | Lösung | Bearbeiter |
| ----------- | ---------- | ---------- | ---------- |
|  10.06.2026 | überall einen 500 Internal Server Error erhalten | In model.py wurden neue variablen hinzugefügt, die nicht in router.py ergängt worden sind. Wurden ergänzt. Jetzt funktioniert wieder alles. |  Aleksandra Vidovic  |
|  11.06.2026 | Users POST-Login hat nicht funktioniert. 500 Internal Server Error | Bei der Klasse UserLogin, war password statt passwort und in der Zeile 118 bei der if-verzweigung hat die Klammer nach dem if gefehlt, um einzutragen was geprüft werden soll. 
|  11.06.2026 | 500 Internal Server Error bei Ordner | Momentan nur in GET Und POST gelöst | habe eine update_db.py erstellt und gefragt und nachgefragt, wie man das lösen kann und habe den code kopiert und es hat dann farbe und title hinzugefügt | Aleksandra Vidovic |
| 11.06.2026 | 500 Internal Server bei GET - ordnerid | Habe in der base.py die zeile 32 von ordnerid zu userid verändert. Die ID war falsch. | Aleksandra Vidovic |
| 11.06.2026 | 500 Internal Server Error bei Karteikarten | Ich habe in der update_db.py den code verändert mit Hilfe, für Karteikarten | Aleksandra Vidovic | 
| 11.06.2026 | 500 Internal Server Error bei Quiz | Habe in update_db.py mit Hilfe den Code umgeschrieben. Zwei Endpunkte funktionieren noch nicht richtig. | Aleksandra Vidovic |
| 11.06.2026 | 500 Internal Server Error bei Statistik | Habe in update_db.py mit Hilfe den Code umgeschrieben | Aleksandra Vidovic |


4.3	Ergebnisse, Interpretation (Tests)
Wie läuft das Programm?
Welche Schwachstellen hat es?   (z.B. Programmlauf nicht flüssig)
## noch schreiben
 
5	Anleitung
5.1	Installationsanleitung
Was muss alles installiert werden 
- PyCharm/Python
- requirements.txt (sind verschiedene installationen vorhanden)

5.2	Bedienungsanleitung
Muss so genau sein, dass auch ein neuer, unbedarfter Benutzer damit zurechtkommt.

Erklärung:
## ? 
 Man muss sich registriernen, wenn man noch kein Account hat, ansonsten kann man sich anmelden mit benutzername und passwort. Wenn man sich registriert oder angemolden hat, dann erscheint ein Fenster, wo man einen Ordner erstellen kann. Man kann in diesem Ordner Karteikarten erstellen, wie offene Fragen, Multiple Choice und True/False. Aus diesen Karteikarten, kann man sich ein Quiz erstellen lassen und daraus lässt sich dann in der Statistik sehen, wie viele Fragen man richtig und wie viele Fragen man falsch hatte. 



6	Bekannte Bugs, Probleme
Welche Bugs liegen noch vor? Warum konnten sie nicht behoben werden?
# falls etwas vorliegen würde, hier notieren. 




 
7	Erweiterungsmöglichkeiten
Wenn ihr noch Zeit hättet, was würdet ihr verbessern oder erweitern?
# vielleicht noch dazu schreiben
 
8	Info

•	Der Zeitplan ist wöchentlich auszufüllen!
•	Endabgabe: dieses Dokument und Projektverzeichnis per Teams abgeben
•	Projektbenotung: Neben dem Endprodukt werden vor allem der Projektfortgang, die Arbeitsweise und die Termintreue benotet (keine Projekte, die in der letzten Nacht fertiggestellt werden!) Der Code soll möglichst übersichtlich gehalten werden (Einsatz von Funktionen und Klassen).

Viel Spaß und happy coding!

   
