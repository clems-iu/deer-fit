from klassen.mitglieder import Mitglied
from klassen.kurse import Kurs
import json
import os

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

    def lade_initialdaten(self):
        """Lädt initiale Daten aus JSON Dateien. Sucht zuerst in /initial/saves/, dann in /initial/basic/"""
        dateien = ['mitglieder.json', 'kurse.json']
        # Eigentlich, aber noch nicht voll entwickelt: dateien = ['mitglieder.json', 'kurse.json', 'bilanz.json', 'trainer.json', 'equipment.json']
        pfade = {}
        
        for datei in dateien:
            basis_pfad = os.path.dirname(__file__)
            pfad_saves = os.path.join(basis_pfad, '..', 'initial', 'saves', datei)
            pfad_basic = os.path.join(basis_pfad, '..', 'initial', 'basic', datei)
            
            try:
                with open(pfad_saves, 'r') as f:
                    pfade[datei] = pfad_saves
            except FileNotFoundError:
                try:
                    with open(pfad_basic, 'r') as f:
                        pfade[datei] = pfad_basic
                except FileNotFoundError:
                    raise FileNotFoundError(f"Datei {datei} nicht gefunden in saves/ oder basic/")
        
        with open(pfade['mitglieder.json'], 'r') as f:
            for md in json.load(f):
                mitglied = Mitglied(md['vorname'], md['nachname'], md['mitgliedsnummer'], md['trainingsfortschritt'], md['mitgliedschaft'])
                self.mitglieder.append(mitglied)
        
        with open(pfade['kurse.json'], 'r') as f:
            for kd in json.load(f):
                kurs = Kurs(kd['name'], kd['beschreibung'], kd['dauer'], kd['max_teilnehmer'], kd['offene_termine'])
                self.kurse.append(kurs)
        
        #with open(pfade['bilanz.json'], 'r') as f:
        #    self.bilanz = json.load(f)

    def speichere_daten(self):
        """Speichert den aktuellen Stand der Daten in /initial/saves/"""
        with open('initial/saves/mitglieder.json', 'w') as f:
            json.dump([vars(m) for m in self.mitglieder], f, indent=2)
        
        with open('initial/saves/kurse.json', 'w') as f:
            json.dump([vars(k) for k in self.kurse], f, indent=2)
        
        #with open('initial/saves/bilanz.json', 'w') as f:
        #    json.dump(self.bilanz, f, indent=2)