# Enthält die Klasse für Trainer im Deer-Fit System

class Trainer:
	def __init__(self, name, fachgebiet, honorar):
		self.name = name
		self.fachgebiet = fachgebiet
		self.honorar = honorar

	def __str__(self):
		return f"Trainer: {self.name} ({self.fachgebiet}), Honorar: {self.honorar} EUR"
