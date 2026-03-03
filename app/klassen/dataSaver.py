import json
import logging
from pathlib import Path
from typing import Any, List

class DataSaver:
    def __init__(self, saves_path: str = "app/saves"):
        self.saves_path = Path(saves_path)
        self.logger = logging.getLogger(self.__class__.__name__)
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    
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

    def save_user(self, user_data: dict) -> bool:
        """Speichert einen neuen User im user_data-Ordner"""
        user_id = str(user_data.get("mitgliedsnummer"))
        file_path = self.saves_path / "user_data" / user_id / "user.json"
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=4)
            self.logger.info(f"Saved user data for user {user_id} to {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving user data for user {user_id} to {file_path}: {e}", exc_info=True)
            return False

    def save_course(self, course_data: dict) -> bool:
        """Speichert einen neuen Kurs im kurse-Ordner"""
        course_id = str(course_data.get("id"))
        file_path = self.saves_path / "studio_data" / "kurse" / course_id / "details.json"
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(course_data, f, ensure_ascii=False, indent=4)
            self.logger.info(f"Saved course data for course {course_id} to {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving course data for course {course_id} to {file_path}: {e}", exc_info=True)
            return False