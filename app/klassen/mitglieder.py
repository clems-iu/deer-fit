# Enthält die Klassen für Mitglieder, Trainingsfortschritte und Mitgliedschaften im Deer-Fit System.


class Mitglied:

    # Selectbox mit den Trainingszielen: Allgemein, Muskelaufbau, Abnehmen, Beweglichkeit ->

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
            self.mitgliedsnummer = self.name_to_id(
                self.vorname + " " + self.nachname
            )  # Generiert eine eindeutige Mitgliedsnummer
        else:
            self.mitgliedsnummer = mitgliedsnummer
        self.trainingsfortschritt = trainingsfortschritt
        self.mitgliedschaft = mitgliedschaft

    def __str__(self):
        return (
            f"{self.vorname} {self.nachname} (Mitgliedsnummer: {self.mitgliedsnummer})"
        )

    def trainingsfortschritt_hinzufuegen(self, fortschritt):
        self.trainingsfortschritt.append(fortschritt)

    def name_to_id(self, name: str) -> int:
        # Name in Bytes (UTF-8)
        b = name.encode("utf-8")
        # Bytes als große Zahl interpretieren
        return int.from_bytes(b, byteorder="big")


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


class Mitgliedschaft:
    def __init__(self, typ, startdatum, enddatum):
        self.typ = typ
        self.startdatum = startdatum
        self.enddatum = enddatum

    def __str__(self):
        return f"Mitgliedschaft: {self.typ} von {self.startdatum} bis {self.enddatum}"
