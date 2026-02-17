# Enthält die Klassen für Mitglieder, Trainingsfortschritte und Mitgliedschaften im Deer-Fit System.

class Mitglied:
    def trainingsplan_empfehlung(self, ziel="Allgemein", fortschritt=None):
        # Kreative, einfache Logik für Trainingsplan-Empfehlung
        if fortschritt is None:
                fortschritt = self.trainingsfortschritt
        if ziel == "Muskelaufbau":
            return [
                "3x/Woche Krafttraining (Ganzkörper)",
                "1x/Woche Ausdauer (z.B. Spinning)",
                "Proteinreiche Ernährung"
                ]
        elif ziel == "Abnehmen":
            return [
                "2x/Woche HIIT oder Ausdauerlauf",
                "2x/Woche Krafttraining",
                "Kaloriendefizit, viel Gemüse"
                ]
        elif ziel == "Beweglichkeit":
            return [
                "2x/Woche Yoga oder Pilates",
                "1x/Woche Stretching",
                "Leichte Cardio-Einheiten"
                ]
        else:
            return [
                "2x/Woche Krafttraining",
                "1x/Woche Ausdauer",
                "1x/Woche Kurs nach Wahl"
            ]
                
    def __init__(self, vorname, nachname, mitgliedsnummer, trainingsfortschritt=[], mitgliedschaft={}):
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