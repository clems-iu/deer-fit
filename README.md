# Aufgabe 8: DeerFit – Das Fitnessstudio des Hirsches

## Idee
Ein Streamlit GUI mit einer Admin- und Mitglieder-Ansicht zur Verwaltung eines Fitnessstudios, dessen Daten objektorientiert verwaltet und in json-Dateien gespeichert werden. 

## Aufgabe
Erstelle eine Python-basierte Anwendung, in der Diego, der Hirsch, ein Fitnessstudio auf der Waldlichtung eröffnet und Code verwendet, um:

- Mitgliedschaften zu verwalten (Tiernamen, Mitgliedschaftstyp, Ablaufdatum)
- Kurspläne zu erstellen (Yoga, Krafttraining, Ausdauerlauf, Schwimmkurse)
- Kursbuchungen abzuwickeln (Anmeldungen, Wartelisten, Absagen)
- Trainingsfortschritte zu dokumentieren (Gewicht, Ausdauer, persönliche Rekorde)
- Gewinne und Ausgaben zu erfassen (Mitgliedsbeiträge, Gerätekosten, Trainerhonorare)
- Fitnessberichte zu visualisieren (Fortschrittskurven der letzten Monate)
- Klassen für Mitglieder, Kurse, Trainer und Geräte zu verwenden
- Personalisierte Trainingspläne zu empfehlen (basierend auf Zielen und Fortschritt) 

## Informationen für die Nutzung
- Die Login-Informationen für die Admin-Sicht sind username: admin, passwort: admin
- Die Anmeldung für User läuft über die Eingabe des Vor- und Nachnamens als username und ein beliebiges Passwort
    - Beispielsweise ein User mit hinterlegten Testdaten, dessen Nutzung sich anbieten würde wäre:
        - Username: Rudy Rentier
        - Passwort: beliebige Zeichenkette 
- Die Speicherung von Daten ist persistent, also werden getätigte Aktionen, wie beispielsweise Buchungen für zukünftige Sessions gespeichert
- Sowohl Kurs-, als auch Userdaten sind in Ordnern, der ihre id tragen im jeweiligen Ordner unter app/saves hinterlegt
- Aktuell können nur Daten hinzugefügt werden, die Löschung / das Updaten von Daten sind technisch vorhanden, konnten aber zeitlich nicht mehr ins UI eingebunden werden 
- Testing ist anhand von Unittests und Integrationstests implementiert, Unittests beispielhaft anhand der zentralen Klasse jsonFolderRepository


## Voraussetzungen
- Python 3.8+
- Abhängigkeiten in `requirements.txt`

## Installation
1. Projektordner in einem Terminal öffnen. 
2. Nach Bedarf eine lokale Environment für Installation erstellen:

```bash
python3 -m venv .venv
.venv\Scripts\Activate.ps1
```
3. Installation der nötigen Pakete:
```bash
pip install -r requirements.txt
```

## Start
```bash
streamlit run main.py
```

Die Web-App ist standardmäßig unter http://localhost:8501 erreichbar.

## Testing
Im Projektordner folgendes ausführen:

```bash
pytest 
```