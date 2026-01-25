#Enthält die Klassen für Kurse, Kurstermine Kursbuchungen und Kurspläne im Deer-Fit System.

class Kurs:
    def __init__(self, name, beschreibung, dauer, max_teilnehmer=10):
        self.name = name
        self.beschreibung = beschreibung
        self.dauer = dauer  # Dauer in Minuten
        self.max_teilnehmer = max_teilnehmer  # Maximale Teilnehmeranzahl
        self.offene_termine = []  # Liste der Kurstermine
        
    def __str__(self):
        return f"{self.name}: {self.beschreibung} ({self.dauer} Minuten)"

class Kurstermin:
    def __init__(self, kurs, datum, uhrzeit):
        self.kurs = kurs
        self.datum = datum  # Datum des Kurstermins
        self.uhrzeit = uhrzeit  # Uhrzeit des Kurstermins
        self.teilnehmer = []  # Liste der angemeldeten Mitglieder

    def teilnehmer_hinzufuegen(self, mitglied):
        if len(self.teilnehmer) < self.kurs.max_teilnehmer:
            self.teilnehmer.append(mitglied)
        else:
            print("Kurs ist voll!")

    def teilnehmer_entfernen(self, mitglied):
        self.teilnehmer.remove(mitglied)

    def __str__(self):
        return f"{self.kurs.name} am {self.datum} um {self.uhrzeit} mit {len(self.teilnehmer)}/{self.kurs.max_teilnehmer} Teilnehmern"
    
        
class Kursbuchung:
    def __init__(self, mitglied, kurs, datum):
        self.mitglied = mitglied
        self.kurs = kurs
        self.datum = datum  # Datum der Kursbuchung

    def __str__(self):
        return f"{self.mitglied} hat sich für {self.kurs} am {self.datum} angemeldet."
    
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
            
            