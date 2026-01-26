from klassen.mitglieder import Mitglied
from klassen.kurse import Kurs
import json

# Ankerpunkt für die DeerFit Anwendung

class DeerFit:
    def __init__(self):
        self.kurse = []      # Liste aller Kurse
        self.mitglieder = []  # Liste aller Mitglieder
        self.user = None     # Aktuell eingeloggtes Mitglied
        self.admin = False   # Admin-Status des eingeloggten Benutzers
        self.bilanz = {}    # Bilanzdaten des Deer-Fit Systems
        

    def user_einloggen(self, mitglied, admin=False):
        self.user = mitglied
        self.admin = admin

    def user_anzeigen(self):
            print(self.user)

    def kurse_anzeigen(self):
        for kurs in self.kurse:
            print(kurs)

    #Lädt aus json Dateien initiale Daten für Mitglieder, Kurse, Bilanz, Equipment und Trainer
    def lade_initialdaten(self, mitgliederpfad, kursepfad, bilanzpfad, trainerpfad, equipmentpfad):
        

        with open(mitgliederpfad, 'r') as f:
            mitglieder_daten = json.load(f)
            for md in mitglieder_daten:
                mitglied = Mitglied(md['vorname'], md['nachname'], md['mitgliedsnummer'], md['trainingsfortschritt'], md['mitgliedschaft'])
                self.mitglieder.append(mitglied)

        with open(kursepfad, 'r') as f:
            kurse_daten = json.load(f)
            for kd in kurse_daten:
                kurs = Kurs(kd['name'], kd['beschreibung'], kd['dauer'], kd['max_teilnehmer'], kd['offene_termine'])
                self.kurse.append(kurs)

        with open(bilanzpfad, 'r') as f:
            self.bilanz = json.load(f)

        # Trainer und Equipment können hier ebenfalls geladen werden
        # Implementierung abhängig von noch zu entwerfenden Klassen und Datenstrukturen