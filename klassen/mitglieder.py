# Enthält die Klassen für Mitglieder, Trainingsfortschritte und Mitgliedschaften im Deer-Fit System.

class Mitglied:
    def __init__(self, vorname, nachname, mitgliedsnummer, trainingsfortschritt=[], mitgliedschaft=[]):
        self.vorname = vorname
        self.nachname = nachname
        self.mitgliedsnummer = mitgliedsnummer
        self.trainingsfortschritt = trainingsfortschritt
        self.mitgliedschaft = mitgliedschaft

    def __str__(self):
        return f"{self.vorname} {self.nachname} (Mitgliedsnummer: {self.mitgliedsnummer})"  
    
    def trainingsfortschritt_hinzufuegen(self, fortschritt):
        self.trainingsfortschritt.append(fortschritt)
    
class Trainingsfortschritt:
    def __init__(self, datum, übung, max):
        self.datum = datum
        self.übung = übung
        self.max = max

    def __str__(self):
        return f"Am {self.datum}: {self.übung} (Bester Wert: {self.max})"
    
class Mitgliedschaft:
    def __init__(self, typ, startdatum, enddatum):
        self.typ = typ
        self.startdatum = startdatum
        self.enddatum = enddatum

    def __str__(self):
        return f"Mitgliedschaft: {self.typ} von {self.startdatum} bis {self.enddatum}"