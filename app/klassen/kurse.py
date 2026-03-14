#Enthält die Klassen für Kurse, Kurstermine und Kurspläne im Deer-Fit System.

import uuid

class Kurs:
    def __init__(self, name, beschreibung, dauer, max_teilnehmer=10, schwierigkeitsgrad="Mittel", typ="Allgemein", id = None):
        if id is None:
            self.id = str(uuid.uuid4())  # Generiert eine eindeutige Id
        else:
            self.id = id  # Verwendet die übergebene ID für jeden Kurs
        self.name = name
        self.beschreibung = beschreibung
        self.dauer = dauer  # Dauer in Minuten
        self.max_teilnehmer = max_teilnehmer  # Maximale Teilnehmeranzahl
        self.schwierigkeitsgrad = schwierigkeitsgrad  # z.B. "Einfach", "Mittel", "Schwer"
        self.typ = typ  # Kann "Kraft", "Cardio", "Yoga", "Speziell" sein
        
    def __str__(self):
        return f"{self.name}: {self.beschreibung} ({self.dauer} Minuten)"

class Kurstermin:
    def __init__(self, kurs, datum, uhrzeit, kursbuchungen=[], id = None):
        if id is None:
            self.id = str(uuid.uuid4())  # Generiert eine eindeutige Id
        else:
            self.id = id  # Verwendet die übergebene ID für jeden Kurstermin
        self.kurs = kurs
        self.datum = datum  # Datum des Kurstermins
        self.uhrzeit = uhrzeit  # Uhrzeit des Kurstermins
        self.kursbuchungen = kursbuchungen  # Liste der angemeldeten Mitglieder als Mitgliedsnummern

    def teilnehmer_hinzufuegen(self, mitgliedsnummer):
        if len(self.kursbuchungen) < self.kurs.max_teilnehmer:
            self.kursbuchungen.append(mitgliedsnummer)
        else:
            print("Kurs ist voll!")

    def teilnehmer_entfernen(self, mitgliedsnummer):
        if mitgliedsnummer in self.kursbuchungen:
            self.kursbuchungen.remove(mitgliedsnummer)

    def __str__(self):
        return f"{self.kurs.name} am {self.datum} um {self.uhrzeit} mit {len(self.kursbuchungen)}/{self.kurs.max_teilnehmer} Teilnehmern"

        

    def __str__(self):
        return f"{self.mitgliedsnummer} hat sich für {self.kurs} am {self.datum} angemeldet."
    
class Kursplan:
    def __init__(self, start, end, kurstermine=[]):
        self.start = start # Startdatum des Kursplans
        self.end = end # Enddatum des Kursplans
        self.kurstermine = kurstermine # Liste der Kurstermine im Kursplan

    def kurstermin_hinzufuegen(self, kurstermin):
        self.kurstermine.append(kurstermin)
        
    def kurstermin_entfernen(self, kurstermin):
        self.kurstermine.remove(kurstermin)    
        
    def alle_termine_anzeigen(self):
        for kurstermin in self.kurstermine:
            print(kurstermin)
            
            