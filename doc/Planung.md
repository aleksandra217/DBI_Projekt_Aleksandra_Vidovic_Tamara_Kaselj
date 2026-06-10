# Planung
## Projektidee: Karteikartensystem 

In unserem Projekt erstellen wir ein Karteikartensystem. Man kann Ordner erstellen und darin Karteikarten speichern. Außerdem kann man Quizze machen und sich eine Statistik anschauen. Es gibt verschiedene Karteikarten-Arten, zum Beispiel Textbox-Karten, Multiple-Choice-Karten und offene Fragen mit Selbstbewertung.


## Ordner: 
- Ein Ordner gehört genau einem User.
- In diesem Ordner können 0...n Karteikarten erstellt werden /sich im Ordner befinden. 
- In diesem Ordner können 0...n Quizze erstellt werden /sich im Ordner befinden. 

## Karteikarten: 
- Eine Karteikarte gehört genau zu einem Ordner.
- Es können mehrere Karteikarten in einem Ordner erstellt werden.

## Quiz: 
- Quiz/Quizze gehören genau zu einem Ordner. 
- Kann aus mehreren QuizFragen bestehen. 

## Statistik: 
- Die Statistik zeigt dir, deinen Lernfortschritt bzw. den Lernprozess. 
- Man sieht immer eine Statistik für einen Ordner immer, um seinen Lernfortschritt verfolgen zu können. 


## ERM:
![alt text](image-10.png)
## RM: 
![alt text](image-8.png)

## Must Haves und Nice To Have: #

### Must Have: 
- Mehrere Ordner können erstellt werden 
- Mehrere Karteikarten können erstellt werden
- Quizze können erstellt werden, gestartet werden und gemacht werden.
- Der User kann sich anmelden -> Login
- Der User muss sich zuerst registrieren, wenn er noch keinen Account hat.  
- Statistik: Das System speichert immer nach jedem Quiz ab, wie viele Richtige und Falsche Antworten man hate und auch das Datum. -> Aktualisierung.

### Nice To Have: 
- Bei dem Ordner eine Farbe auswählen können
- Limit bei Karteikarten setzen
- Limit bei Erstellung von Quizzes erstellen  


## Aufgabenverteilung: Wer macht was? 
Aleksandra: 
- FastAPI Grundstruktur 
- CRUD Endpunkte 
- Datenbank anlegen und Tabellen erzeugen 
- SQL Constraints definieren.
- für die Statistik Aggregrations-Endpunkte
- Testen aller Datenbankabfragen
- Prüfen der Normalisierung

Tamara: 
- Erstellung der Tabellen in SQLite 
- JOIN Endpunkte 
- Rollen System einbauen- admin/user 
- Fehlerbehandlungen
- Statistiken und Aggregation entwickeln, also Karten pro Ordner und die Quiz Auswertung. 
- Filter-, Such- und Sortiert-Parameter für GET machen
- Überprüfen der Rollen und Berechtigungen

Beide: 
- Testen aller API Endpunkte
- Konsistenz von Statuscodes und Fehlermeldungen überprüfen. 
- Ordner, Karteikarten, Quizze, Statistik Pydantic Modelle machen.

## Git Repository erstellen: wurde erstellt  



## Was macht jede Tabelle: 
User: 
- Speichert die Daten des Users wie die Email Adresse, Name und Passwort.

Ordner: 
- Speichert die vom User erstellen Ordner.

Karteikarte:
- Karteikarte kann man mit drei verschiedenen Typen erstellen: Offene Fragen, True/False und Multiple Choice. Jede Karteikarte gehört fest zu genau einem Ordner. Speichert die Inhalte.

Quiz:
- Repräsentiert ein Quiz, das erstellt worden ist. Wird aus Karteikarten erstellt.

Quiz_Karteikarte_erstellen:
- Verbindet nur die Tabelle Quiz und die Tabelle Karteikarte über die IDs.

Statistik:
- Speichert die Daten vom Lernfortschritt, also die Richtigen und Falschen Antworten und die Aktualisierung der Statistik.

## Normalformen nachweisen: 


Tabelle User: 
- 1.NF: Alle Attribute liegen atomar vor. 
- 2.NF: Es gibt einen PK. 
- 3.NF: Name und die E-Mailadresse hängen nur von der UserID ab und es gibt keine transitiven Abhängigkeiten.

Tabelle Ordner; 
- 1.NF: Alle Attribute liegen atomar vor. 
- 2.NF: Es gibt einen PK.
- 3.NF: Titel und UserId hängen vom Ordner ab. 

Tabelle Karteikarte: 
- 1.NF: Alle Attribute liegen atomar vor. 
- 2.NF: hat einen PK.
- 3.NF: Inhalt der Karteikarte hängt von der KarteikartenID ab und es gibt keine transitiven Abhängigkeiten.

Tabelle Quiz: 
- 1.NF: Titel ist atomar.
- 2.NF: Es gibt einen PK. 
- 3.NF: keine transitiven abhängigkeiten.


Quiz_Karteikarten_erstellen: 
- 1.NF: Atomar.
- 2.NF: Es gibt einen PK.
- 3.NF: Keine abhängigkeiten.

Statistik:
- 1.NF: Atomar.
- 2.NF: Es gibt einen PK.
- 3.NF: keine abhängigkeiten.


