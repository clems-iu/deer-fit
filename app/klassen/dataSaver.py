import json
import logging
from pathlib import Path
from typing import Any, List
from app.klassen.mitglieder import Mitglied
from app.klassen.kurse import Kurs, Kurstermin

class DataSaver:
	def __init__(self, saves_path: str = "app/saves"):
		self.saves_path = Path(saves_path)
		self.logger = logging.getLogger(self.__class__.__name__)
		if not logging.getLogger().hasHandlers():
			logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
			
	def save_course_dates(self, course_id: str, termine: list) -> bool:
		"""Speichert die Terminliste für einen Kurs (überschreibt die termine.json)"""
		file_path = self.saves_path / "studio_data" / "kurse" / str(course_id) / "termine.json"
		try:
			file_path.parent.mkdir(parents=True, exist_ok=True)
			with open(file_path, 'w', encoding='utf-8') as f:
				json.dump(termine, f, ensure_ascii=False, indent=4)
			self.logger.info(f"Saved course dates for course {course_id} to {file_path}")
			return True
		except Exception as e:
			self.logger.error(f"Error saving course dates for course {course_id} to {file_path}: {e}", exc_info=True)
			return False
	
	
	def add_bilanz_data(self, betrag: str, beschreibung: str) -> bool:
		"""Fügt Bilanz-Daten hinzu"""
		file_path = self.saves_path / "studio_data" / "bilanz.json"
		data = {"betrag": betrag, "beschreibung": beschreibung}
		try:
			file_path.parent.mkdir(parents=True, exist_ok=True)
			if file_path.exists():
				with open(file_path, 'r', encoding='utf-8') as f:
					existing_data = json.load(f)
			else:
				existing_data = []
			existing_data.append(data)
			with open(file_path, 'w', encoding='utf-8') as f:
				json.dump(existing_data, f, ensure_ascii=False, indent=4)
			self.logger.info(f"Added bilanz data to {file_path}")
			return True
		except Exception as e:
			self.logger.error(f"Error adding bilanz data to {file_path}: {e}", exc_info=True)
			return False

	def save_user(self, user_data: Mitglied) -> bool:
		"""Speichert einen neuen User im user_data-Ordner"""
		user_id = str(user_data.mitgliedsnummer)
		file_path = self.saves_path / "user_data" / user_id / "user.json"
		try:
			file_path.parent.mkdir(parents=True, exist_ok=True)
			with open(file_path, 'w', encoding='utf-8') as f:
				json.dump(user_data.__dict__, f, ensure_ascii=False, indent=4)
			self.logger.info(f"Saved user data for user {user_id} to {file_path}")
			return True
		except Exception as e:
			self.logger.error(f"Error saving user data for user {user_id} to {file_path}: {e}", exc_info=True)
			return False

	def save_course(self, course_data: Kurs) -> bool:
		"""Speichert einen neuen Kurs im kurse-Ordner"""
		course_id = str(course_data.id)
		file_path = self.saves_path / "studio_data" / "kurse" / course_id / "details.json"
		try:
			file_path.parent.mkdir(parents=True, exist_ok=True)
			with open(file_path, 'w', encoding='utf-8') as f:
				json.dump(course_data.__dict__, f, ensure_ascii=False, indent=4)
			self.logger.info(f"Saved course data for course {course_id} to {file_path}")
			return True
		except Exception as e:
			self.logger.error(f"Error saving course data for course {course_id} to {file_path}: {e}", exc_info=True)
			return False
		
	def save_booking(self, booking_data: dict) -> bool:
		"""Speichert eine neue Buchung im kurse-Ordner unter termine"""
		self.logger.info(f"Saving booking data for booking {booking_data}")
		course_id = str(booking_data.get("kurs_id"))
		file_path = self.saves_path / "studio_data" / "kurse" / course_id / "termine.json"
		try:
			file_path.parent.mkdir(parents=True, exist_ok=True)
			if file_path.exists():
				with open(file_path, 'r', encoding='utf-8') as f:
					existing_data = json.load(f)
			else:
				existing_data = []

			# Die user_id aus booking_data extrahieren
			user_id = booking_data.get("mitgliedsnummer")
			termin_id = booking_data.get("termin_id")

			# Suche den passenden Termin und füge die user_id zu "buchungen" hinzu
			for termin in existing_data:
				if termin.get("id") == termin_id:
					buchungen = termin.setdefault("kursbuchungen", [])
					if user_id and user_id not in buchungen:
						buchungen.append(user_id)
					break

			with open(file_path, 'w', encoding='utf-8') as f:
				json.dump(existing_data, f, ensure_ascii=False, indent=4)
			self.logger.info(f"Saved booking data for course {course_id} to {file_path}")
			return True
		except Exception as e:
			self.logger.error(f"Error saving booking data for course {course_id} to {file_path}: {e}", exc_info=True)
			return False
		
	def save_progress(self, user_id: str, progress_data: dict) -> bool:
		"""Speichert Fortschrittsdaten für einen User"""
		user_id = str(user_id)
		file_path = self.saves_path / "user_data" / user_id / "fortschritte.json"
		try:
			file_path.parent.mkdir(parents=True, exist_ok=True)
			with open(file_path, 'w', encoding='utf-8') as f:
				json.dump(progress_data, f, ensure_ascii=False, indent=4)
			self.logger.info(f"Saved progress data for user {user_id} to {file_path}")
			return True
		except Exception as e:
			self.logger.error(f"Error saving progress data for user {user_id} to {file_path}: {e}", exc_info=True)
			return False
		
	def save_equipment(self, equipment_data: dict) -> bool:
		"""Speichert Equipment-Daten im studio_data-Ordner unter equipment"""
		file_path = self.saves_path / "studio_data" / "equipment.json"
		try:
			file_path.parent.mkdir(parents=True, exist_ok=True)
			if file_path.exists():
				with open(file_path, 'r', encoding='utf-8') as f:
					existing_data = json.load(f)
			else:
				existing_data = []
			
			existing_data.append(equipment_data)
			with open(file_path, 'w', encoding='utf-8') as f:
				json.dump(existing_data, f, ensure_ascii=False, indent=4)
			self.logger.info(f"Saved equipment data to {file_path}")
			return True
		except Exception as e:
			self.logger.error(f"Error saving equipment data to {file_path}: {e}", exc_info=True)
			return False