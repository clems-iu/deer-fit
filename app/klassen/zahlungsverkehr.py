# Enthält Klassen für Einnahmen und Ausgaben im Deer-Fit System

class FinanzEintrag:
	def __init__(self, typ, betrag, kategorie, datum, beschreibung=""):
		self.typ = typ  # "Einnahme" oder "Ausgabe"
		self.betrag = betrag
		self.kategorie = kategorie  # z.B. "Mitgliedsbeitrag", "Gerätekosten", "Trainerhonorar"
		self.datum = datum
		self.beschreibung = beschreibung

	def __str__(self):
		return f"{self.typ}: {self.betrag} EUR für {self.kategorie} am {self.datum} ({self.beschreibung})"

class Finanzverwaltung:
	def __init__(self):
		self.eintraege = []

	def eintrag_hinzufuegen(self, eintrag):
		self.eintraege.append(eintrag)

	def gesamtbilanz(self):
		einnahmen = sum(e.betrag for e in self.eintraege if e.typ == "Einnahme")
		ausgaben = sum(e.betrag for e in self.eintraege if e.typ == "Ausgabe")
		return einnahmen - ausgaben

	def eintraege_nach_typ(self, typ):
		return [e for e in self.eintraege if e.typ == typ]
