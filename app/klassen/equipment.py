# Enthält die Klasse für Geräte im Deer-Fit System

class Geraet:
	def __init__(self, name, anschaffungsjahr, kosten, status="verfügbar"):
		self.name = name
		self.anschaffungsjahr = anschaffungsjahr
		self.kosten = kosten
		self.status = status

	def __str__(self):
		return f"Gerät: {self.name} (Anschaffung: {self.anschaffungsjahr}, Kosten: {self.kosten} EUR, Status: {self.status})"
