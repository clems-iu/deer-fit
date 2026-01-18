# Enthält die Klassen für Mitglieder, Trainingsfortschritte und Mitgliedschaften im Deer-Fit System.

class Mitglied:
    def __init__(self, vorname, nachname, mitgliedsnummer):
        self.vorname = vorname
        self.nachname = nachname
        self.mitgliedsnummer = mitgliedsnummer
        self.trainingsfortschritt = []
        self.mitgliedschaft = []

    def __str__(self):
        return f"{self.vorname} {self.nachname} (Mitgliedsnummer: {self.mitgliedsnummer})"  
    
class trainingsfortschritt:
    def __init__(self, datum, beschreibung):
        self.datum = datum
        self.beschreibung = beschreibung

    def __str__(self):
        return f"Am {self.datum}: {self.beschreibung}"
    
class mitgliedschaft:
    def __init__(self, typ, startdatum, enddatum):
        self.typ = typ
        self.startdatum = startdatum
        self.enddatum = enddatum

    def __str__(self):
        return f"Mitgliedschaft: {self.typ} von {self.startdatum} bis {self.enddatum}"