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

- Speicherungssystem ausdenken, welches sauberen schnellen Zugriff ermöglicht
- Klassen mit Attributen und Funktionen erstellen welche alle nötigen Objekte in diesem System beschreiben
- Basis Initialierung mit einigen Mitgliedern, Trainern, Kursen und Equipment einrichten um initiale Verwendung zu ermöglichen (Erstmal im Terminal, initiale Daten aus csv?)
- Web-UI mit Admin und Usersicht -> Anmeldebildschirm, Routing?
- Trainingsempfehlungen machen -> Hinterlegen, welche Muskelgruppen wann optimal trainiert werden müssten? Oder aus Gewohnheiten der Person ableitend?


# Bisheriger Fortschritt

- Erstellen der Basisdateien
- Füllen der ersten Version der Kurs-Klassen
- Füllen der ersten Version der Mitglied-Klassen
- Entscheidung **streamlit** für UI zu nutzen


# Aufbau der bisher erstellten Klassen

Kursplan 1:n Kurstermine
Kurs 1:n Kurstermin 1:n Kursbuchung 
Mitglied 1:1 Mitgliedschaft
Mitglied 1:n Trainingfortschritte