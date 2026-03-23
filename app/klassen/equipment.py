# Enthält die Klasse für Geräte und Trainer im Deer-Fit System, dadurch, dass die Kosten wiederkehrend sein können, 
# wird die Klasse Equipment erweitert, um gemietete Geräte oder Trainer zu unterstützen.
import uuid

class Equipment:
	def __init__(self, name, anschaffungsdatum, kosten, sindKostenWiederkehrend=False):
		self.id = str(uuid.uuid4())  # Generiert eine eindeutige ID für jedes Equipment
		self.name = name
		self.anschaffungsdatum = anschaffungsdatum
		self.kosten = kosten
		self.sindKostenWiederkehrend = sindKostenWiederkehrend  # Standardmäßig auf False gesetzt
		

	def __str__(self):
		return f"Equipment: {self.name} (Anschaffung: {self.anschaffungsdatum}, Kosten: {self.kosten} EUR, Wiederkehrend: {self.sindKostenWiederkehrend})"

	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"anschaffungsdatum": self.anschaffungsdatum,
			"kosten": self.kosten,
			"sindKostenWiederkehrend": self.sindKostenWiederkehrend
		}
  
	def from_dict(data):
			return Equipment(
				name=data["name"],
				anschaffungsdatum=data["anschaffungsdatum"],
				kosten=data["kosten"],
				sindKostenWiederkehrend=data.get("sindKostenWiederkehrend", False)  # Standardwert False, falls nicht vorhanden
			)