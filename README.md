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
- Personalisierte Trainingspläne zu empfehlen (basierend auf Zielen und Fortschritt) *(sei hier kreativ)*

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