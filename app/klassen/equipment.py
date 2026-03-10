# Enthält die Klasse für Geräte und Trainer im Deer-Fit System, dadurch, dass die Kosten wiederkehrend sein können, 
# wird die Klasse Equipment erweitert, um gemietete Geräte oder Trainer zu unterstützen.
import uuid

class Equipment:
	def __init__(self, name, anschaffungsjahr, kosten, sindKostenWiederkehrend=False):
		self.id = str(uuid.uuid4())  # Generiert eine eindeutige ID für jedes Equipment
		self.name = name
		self.anschaffungsjahr = anschaffungsjahr
		self.kosten = kosten
		self.sindKostenWiederkehrend = sindKostenWiederkehrend  # Standardmäßig auf False gesetzt
		

	def __str__(self):
		return f"Equipment: {self.name} (Anschaffung: {self.anschaffungsjahr}, Kosten: {self.kosten} EUR, Wiederkehrend: {self.sindKostenWiederkehrend})"
