import json
import os
from datetime import date, datetime

# Anmeldedaten für die DeerFit Anwendung


class Authenticator:

    def __init__(self):
        self.authenticated = False
        self.role = None
        self.mitgliedsnummer = None

    def _mitgliedschaft_ist_gueltig(self, user_json_path: str) -> bool:
        with open(user_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        m = data.get("mitgliedschaft")
        if not m:
            return False

        try:
            start = datetime.strptime(m["startdatum"], "%Y-%m-%d").date()
            ende = datetime.strptime(m["enddatum"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            # fehlende oder falsche Datumsangaben
            return False

        heute = date.today()
        return start <= heute <= ende

    def login(self, mitgliedsnummer, password):

        if mitgliedsnummer == "admin" and password == "admin":
            self.authenticated = True
            self.role = "admin"
            return "Erfolgreich als admin eingeloggt"
        else:

            # Pfad zum User-Ordner
            user_data_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "saves",
                "user_data",
                str(mitgliedsnummer),
            )

            user_json_path = os.path.join(user_data_path, "user.json")

            # Prüfen, ob notwendige Verzeichnisse und Dateien existieren
            if not os.path.isdir(user_data_path):
                return (
                    f"Fehler: Der Benutzer wurde nicht gefunden unter: {user_data_path}"
                )

            if not os.path.isfile(user_json_path):
                return "Fehler: Die Daten des Users sind fehlerhaft. Bitte kontaktieren Sie den Support."

            if not self._mitgliedschaft_ist_gueltig(user_json_path):
                return "Fehler: Die Mitgliedschaft ist abgelaufen oder ungültig."

            # Optional: Passwortüberprüfung hinzufügen
            self.authenticated = True
            self.role = "user"
            self.mitgliedsnummer = mitgliedsnummer
            return "Erfolgreich eingeloggt"

    def logout(self):
        self.authenticated = False
        self.role = None
        self.mitgliedsnummer = None
