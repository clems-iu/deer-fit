# Enthält die Klassen für Mitglieder, Trainingsfortschritte und Mitgliedschaften im Deer-Fit System.

# Die Mitgliedsklasse repräsentiert ein Mitglied des Fitnessstudios, einschließlich persönlicher Informationen, Trainingsfortschritt und Mitgliedschaftsdaten.
class Mitglied:

    def __init__(
        self,
        vorname,
        nachname,
        trainingsfortschritt=[],
        mitgliedschaft={},
        mitgliedsnummer=None,
    ):
        self.vorname = vorname
        self.nachname = nachname
        if mitgliedsnummer is None:
            self.mitgliedsnummer = self.name_to_id(self.vorname + " " + self.nachname)
        else:
            self.mitgliedsnummer = mitgliedsnummer
        self.trainingsfortschritt = trainingsfortschritt
        self.mitgliedschaft = mitgliedschaft

    def __str__(self):
        return (
            f"{self.vorname} {self.nachname} (Mitgliedsnummer: {self.mitgliedsnummer})"
        )

    def name_to_id(self, name: str) -> int:
        """Generiert eine eindeutige ID basierend auf dem Namen des Mitglieds."""
        b = name.encode("utf-8")
        return int.from_bytes(b, byteorder="big")

    def from_dict(data: dict) -> "Mitglied":
        return Mitglied(
            vorname=data["vorname"],
            nachname=data["nachname"],
            trainingsfortschritt=[
                Trainingsfortschritt.from_dict(tf)
                for tf in data.get("trainingsfortschritt", [])
            ],
            mitgliedschaft=data.get("mitgliedschaft", {}),
            mitgliedsnummer=data.get("mitgliedsnummer"),
        )

    def to_dict(self) -> dict:
        return {
            "vorname": self.vorname,
            "nachname": self.nachname,
            "trainingsfortschritt": [tf.to_dict() for tf in self.trainingsfortschritt],
            "mitgliedschaft": self.mitgliedschaft,
            "mitgliedsnummer": self.mitgliedsnummer,
        }

# Die Trainingsfortschritt-Klasse repräsentiert den Fortschritt eines Mitglieds bei einer bestimmten Übung, einschließlich Datum, Übung, Bestleistung, Einheit und Wiederholungen.
class Trainingsfortschritt:
    def __init__(self, datum, übung, best, einheit, reps):
        self.datum = datum
        self.übung = übung
        self.best = best
        self.einheit = einheit
        self.reps = reps

    def from_dict(data: dict) -> "Trainingsfortschritt":
        return Trainingsfortschritt(
            datum=data["datum"],
            übung=data["übung"],
            best=data["best"],
            einheit=data["einheit"],
            reps=data["reps"],
        )

    def to_dict(self) -> dict:
        return {
            "datum": self.datum,
            "übung": self.übung,
            "best": self.best,
            "einheit": self.einheit,
            "reps": self.reps,
        }


# Die Mitgliedschaft-Klasse repräsentiert die Art der Mitgliedschaft eines Mitglieds, einschließlich des Typs, Start- und Enddatums.
class Mitgliedschaft:
    def __init__(self, typ, startdatum, enddatum):
        self.typ = typ
        self.startdatum = startdatum
        self.enddatum = enddatum

    def __str__(self):
        return f"Mitgliedschaft: {self.typ} von {self.startdatum} bis {self.enddatum}"
