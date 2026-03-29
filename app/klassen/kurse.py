# Enthält die Klassen für Kurse und Kurstermine im Deer-Fit System.

import uuid

# Die Klasse "Kurs" repräsentiert einen Kurs mit seinen Eigenschaften wie Name, Beschreibung, Dauer, etc.
class Kurs:
    def __init__(
        self,
        name,
        beschreibung,
        dauer,
        max_teilnehmer=10,
        schwierigkeitsgrad="Mittel",
        typ="Allgemein",
        id=None,
    ):
        if id is None:
            self.id = str(uuid.uuid4())  # Generiert eine eindeutige Id
        else:
            self.id = id  # Verwendet die übergebene ID für jeden Kurs
        self.name = name
        self.beschreibung = beschreibung
        self.dauer = dauer  # Dauer in Minuten
        self.max_teilnehmer = max_teilnehmer  # Maximale Teilnehmeranzahl
        self.schwierigkeitsgrad = (
            schwierigkeitsgrad  # z.B. "Einfach", "Mittel", "Schwer"
        )
        self.typ = typ  # Kann "Kraft", "Cardio", "Yoga", "Speziell" sein

    def __str__(self):
        return f"{self.name}: {self.beschreibung} ({self.dauer} Minuten)"

    def from_dict(data: dict) -> "Kurs":
        return Kurs(
            name=data["name"],
            beschreibung=data["beschreibung"],
            dauer=data["dauer"],
            max_teilnehmer=data.get("max_teilnehmer", 10),
            schwierigkeitsgrad=data.get("schwierigkeitsgrad", "Mittel"),
            typ=data.get("typ", "Allgemein"),
            id=data.get("id"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "beschreibung": self.beschreibung,
            "dauer": self.dauer,
            "max_teilnehmer": self.max_teilnehmer,
            "schwierigkeitsgrad": self.schwierigkeitsgrad,
            "typ": self.typ,
        }


# Die Klasse "Kurstermin" repräsentiert einen spezifischen Termin für einen Kurs, inklusive Datum, Uhrzeit und angemeldeten Teilnehmern.
class Kurstermin:
    def __init__(self, datum, uhrzeit, kursId, kursbuchungen=[], id=None, kurs={}):
        if id is None:
            self.id = str(uuid.uuid4())  # Generiert eine eindeutige Id
        else:
            self.id = id  # Verwendet die übergebene ID für jeden Kurstermin
        self.kursId = kursId
        self.datum = datum  # Datum des Kurstermins
        self.uhrzeit = uhrzeit  # Uhrzeit des Kurstermins
        self.kursbuchungen = (
            kursbuchungen  # Liste der angemeldeten Mitglieder als Mitgliedsnummern
        )
        self.kurs = kurs  # Kursdetails, z.B. Name, Beschreibung, Dauer, etc.

    def teilnehmer_hinzufuegen(self, mitgliedsnummer):
        """Fügt einen Teilnehmer zum Kurstermin hinzu, wenn die maximale Teilnehmerzahl nicht überschritten wird."""
        if len(self.kursbuchungen) < self.kurs.max_teilnehmer:
            self.kursbuchungen.append(mitgliedsnummer)
        else:
            print("Kurs ist voll!")

    def teilnehmer_entfernen(self, mitgliedsnummer):
        if mitgliedsnummer in self.kursbuchungen:
            self.kursbuchungen.remove(mitgliedsnummer)

    def from_dict(data: dict) -> "Kurstermin":
        return Kurstermin(
            kursId=data.get("kursId"),
            datum=data["datum"],
            uhrzeit=data["uhrzeit"],
            kursbuchungen=data.get("kursbuchungen", []),
            id=data.get("id"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "kursId": self.kursId,
            "datum": self.datum,
            "uhrzeit": self.uhrzeit,
            "kursbuchungen": self.kursbuchungen,
        }
