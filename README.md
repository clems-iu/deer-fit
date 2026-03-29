# 🦌 DeerFit – Das Fitnessstudio des Hirsches

##  Projektüberblick
**DeerFit** ist eine Python-basierte Fitnessstudio-Verwaltungsanwendung mit einem **Streamlit-GUI**, die sowohl eine **Admin-Ansicht** als auch eine **Mitglieder-Ansicht** bietet. 
Die Anwendung nutzt **objektorientierte Programmierung** und speichert alle Daten **persistent in JSON-Dateien**. Zentral sind die meisten für die **Portfolio-Bewertung** nötigen Informationen hier in dieser Datei zu finden. Ergänzendes Material ist im Ordner `portfolio/` hinterlegt. Die Schritte unter **Inbetriebnahme** können unter anderen Betriebssystemen als Windows ggf. abweichen.

---

##  Ziel der Anwendung
Die Anwendung simuliert ein Fitnessstudio, das von *Diego dem Hirsch* betrieben wird, und ermöglicht die digitale Verwaltung zentraler Studiofunktionen:

- Verwaltung von Mitgliedschaften
- Planung und Organisation von Kursen
- Buchungssystem inkl. Wartelisten
- Tracking von Trainingsfortschritten
- Finanzübersicht (Einnahmen & Ausgaben)
- Visualisierung von Fitnessdaten
- Personalisierte Trainingspläne

---

##  Angestrebte Kernfunktionen

###  Mitgliederverwaltung
- Erstellung und Speicherung von Mitgliederdaten

###  Kursmanagement
- Erstellung und Verwaltung von Kursen

###  Buchungssystem
- Kursanmeldungen
- Wartelistenverwaltung
- Stornierungen

###  Trainingsfortschritt
- Dokumentation von Trainingsrekorden

###  Datenvisualisierung
- Darstellung von Fortschrittsverläufen

###  Finanzverwaltung
- Einnahmen:
  - Mitgliedsbeiträge
- Ausgaben:
  - Gerätekosten
  - Trainerhonorare

###  Personalisierte Trainingspläne
- Empfehlung basierend auf:
  - bisherigen Kursen

---

##  Technische Architektur

### Objektorientierte Struktur
- Die Anwendung verwendet zentral Klassen wie:
    - `Mitglied`
    - `Kurs`
    - `Equipment`
- Und zentral zur internen Verwaltung der json-Dateien Klassen wie:
    - `JsonFolderRepository`
    - `JsonListRepository`

###  Persistenz
- Speicherung aller Daten in **JSON-Dateien**
- Kern-Struktur:
    - app/saves/
        - ├── user_data/<user_id>/
        - └── studio_data/kurse/<kurs_id>/

- Daten bleiben auch nach Neustart erhalten

---

##  Nutzung & Zugang

### Admin-Zugang
- **Username:** `admin`
- **Passwort:** `admin`

### Benutzer-Login
- Login erfolgt über:
- Vorname + Nachname als Username
- beliebiges Passwort

**Beispiel-Testnutzer:**
- Username: `Rudy Rentier`
- Passwort: frei wählbar (wird aktuell nicht geprüft)

### Austestbare Funktionen
- Login als Admin oder Mitglied
- In der Admin-Ansicht können Mitglieder, Kurse, Equipment und Finanzen verwaltet werden
- In der User-Ansicht können Kurse gebucht und Trainingsfortschritte betrachtet, sowie hinzugefügt werden 

---

##  Aktuelle Einschränkungen und Known Bugs
- Kernfunktionen sind implementiert bis auf Kurswarteschlange/Stornierung von Buchungen
- Update- und Löschfunktionen sind implementiert, aber aktuell noch nicht im UI verfügbar
- Teilweise lädt der streamlit_calendar eher langsam, was zu visuellen Fehlern führen kann, die sich allerdings nach wenigen Sekunden selbst lösen
- Kursempfehlungen können gerade nur angezeigt werden, wenn sich durch bisherige Buchungen eine Entwicklung abzeichnet (mindestens 3 Buchungen in einem Kurstyp mit nicht der gleichen Schwierigkeit, bspw. Spinning leicht, Spinning leicht, Spinning mittel)


---

## Erweiterungsmöglichkeiten
- Mehrsprachigkeit
- Mobile Ansicht
- Verwaltung der Trainer-Anwesenheiten und Abrechnung dementsprechend
- Export der Abrechnung und Einsehen alter Abrechnungen
- Auswertung der Kursnachfrage für Zukunftsplanung von Kursterminen 


---

## Inbetriebnahme

###  Voraussetzungen
- Python: Version 3.8 oder höher
- Abhängigkeiten: siehe requirements.txt

###  Installation
1. Projektordner im Terminal öffnen
2. (Optional) Virtuelle Umgebung erstellen:
```bash
python3 -m venv .venv
.venv\Scripts\Activate.ps1
```
3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

###  Anwendung starten
```bash
streamlit run main.py
```

➡️ Die Anwendung ist anschließend erreichbar unter:
http://localhost:8501

---

##  Testing

### Implementiert:
- Pytest Einbindung zur Verwaltung der Tests
- Unit Tests beispielhaft an zentraler Klasse: `jsonFolderRepository`
- 3 Integrationstests


### Ausführen:
```bash
pytest
```