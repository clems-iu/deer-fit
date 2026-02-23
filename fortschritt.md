# Funktionen

- Mitgliedschaften verwalten (Tiernamen, Mitgliedschaftstyp, Ablaufdatum)
- Kurspläne erstellen (Yoga, Krafttraining, Ausdauerlauf, Schwimmkurse)
- Kursbuchungen abwickeln (Anmeldungen, Wartelisten, Absagen)
- Trainingsfortschritte dokumentieren (Gewicht, Ausdauer, persönliche Rekorde)
- Gewinne und Ausgaben erfassen (Mitgliedsbeiträge, Gerätekosten, Trainerhonorare)
- Fitnessberichte visualisieren (Fortschrittskurven der letzten Monate)
- Klassen für Mitglieder, Kurse, Trainer und Geräte verwenden
- Personalisierte Trainingspläne empfehlen (basierend auf Zielen und Fortschritt) *(sei hier kreativ)*


# Umsetzung

- Speicherungssystem ausdenken, welches sauberen schnellen Zugriff für alle Screens ermöglicht
    - Speicherung in Dateien (Kurse, Mitglieder, Buchungen)
- Klassen mit Attributen und Funktionen erstellen welche alle nötigen Objekte in diesem System beschreiben
- Basis Initialierung mit einigen Mitgliedern, Trainern, Kursen und Equipment einrichten um initiale Verwendung zu ermöglichen (Erstmal im Terminal, initiale Daten aus csv?)
- Trainingsempfehlungen machen -> Hinterlegen, welche Muskelgruppen wann optimal trainiert werden müssten? Oder aus Trainingszielen der Person ableitend? 

- Web-UI mit Admin und Usersicht -> Anmeldebildschirm, Routing?
    - User hat gebuchte Kurse, Kursplan, Fortschritte und Trainingsempfehlungen
    - Admin hat Kostenverlauf, Ausstattung, Belegung und Kursplan mit mehr Details


# Bisheriger Fortschritt

- Erstellen der Basisdateien
- Füllen der ersten Version der Kurs-Klassen
- Füllen der ersten Version der Mitglied-Klassen
- Entscheidung **streamlit** für UI zu nutzen,  Matplotlib für Graphen
- Erstellung einer Klasse DeerFit, welche die Systemdaten bündelt und auch zur initialisierung genutzt werden kann
- Erstellung der noch übrigen Klassen (Bilanzen, Trainer, Equipment...)
- Erste Login, User und Admin Seite mit streamlit (Unterseiten und Rahmendiv erstellt, Daten größtenteils noch nicht aufbereitet)
- Erster Versuch Fortschritt und Vorschläge zu modellieren
- #deprecated Initiale Datenauslese aus json-Dateien (Für Kurse und Mitglieder erstmal) 
- #deprecated Noch ergänzen um Abfrage für jedes Mal wenn Daten angefordert werden, damit konsistent 
- Neu:
	- Anmeldung bestimmter User ermöglichen
	- Simultan mehrere User erlauben
	- Neues Speichersystem mit Möglichkeit pro User Daten abzurufen
		- Einbindung dieses Systems in User-Ansicht

# Nächste Schritte

- Datenspeicherung
- Bilanzen, Trainer und Equipment einbauen
- Fortschrittsmodell verallgemeinern
- Vorhersagemodell für nächste Kurse
- Testing



# Aufbau der bisher erstellten Klassen

- Kursplan 1:n Kurstermine
- Kurs 1:n Kurstermin 1:n Kursbuchung 
- Mitglied 1:1 Mitgliedschaft
- Mitglied 1:n Trainingfortschritte
