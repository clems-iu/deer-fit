import json
import logging
from pathlib import Path
from typing import Any, List

class DataLoader:
    def __init__(self, saves_path: str = "app/saves"):
        self.saves_path = Path(saves_path)
        self.logger = logging.getLogger(self.__class__.__name__)
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    
    def load_studio_data(self, filename: str) -> dict | List:
        """Lädt Daten aus dem studio_data Ordner"""
        file_path = self.saves_path / "studio_data" / f"{filename}.json"
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.info(f"Loaded studio data from {file_path}")
                    return data
            else:
                self.logger.warning(f"File not found: {file_path}")
        except Exception as e:
            self.logger.error(f"Error loading studio data from {file_path}: {e}", exc_info=True)
        return []
    
    def load_course_data(self, course_id: str, filename: str) -> dict | List:
        """Lädt Daten aus einem spezifischen Kurs"""
        file_path = self.saves_path / "studio_data" / "kurse" / course_id / f"{filename}.json"
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.info(f"Loaded course data from {file_path}")
                    return data
            else:
                self.logger.warning(f"File not found: {file_path}")
        except Exception as e:
            self.logger.error(f"Error loading course data from {file_path}: {e}", exc_info=True)
        return []
    
    def load_all_courses(self) -> List[dict]:
        """Lädt alle Kurse aus den details.json Dateien der einzelnen Kursordner"""
        courses = []
        kurse_dir = self.saves_path / "studio_data" / "kurse"
        try:
            if kurse_dir.exists():
                for course_dir in kurse_dir.iterdir():
                    if course_dir.is_dir():
                        course_data = self.load_course_data(course_dir.name, "details")
                        if course_data:
                            course_data["id"] = course_dir.name
                            courses.append(course_data)
                self.logger.info(f"Loaded all {len(courses)} courses from {kurse_dir}")
            else:
                self.logger.warning(f"Courses directory not found: {kurse_dir}")
        except Exception as e:
            self.logger.error(f"Error loading all courses from {kurse_dir}: {e}", exc_info=True)
        return courses

    def load_course_dates(self, course_id: str, start_date: str = None, end_date: str = None) -> List[dict]:
        """Lädt Kurstermine optional gefiltert nach Zeitraum"""
        termine = self.load_course_data(course_id, "termine")
        if not isinstance(termine, list):
            self.logger.warning(f"Expected list for course dates, got {type(termine)} for course {course_id}")
            return []
        if start_date and end_date:
            filtered = [t for t in termine if start_date <= t.get("datum", "") <= end_date]
            self.logger.info(f"Filtered {len(filtered)} course dates for course {course_id} between {start_date} and {end_date}")
            return filtered
        self.logger.info(f"Loaded {len(termine)} course dates for course {course_id}")
        return termine
    
    def load_user_data(self, user_id: str, filename: str) -> dict | List:
        """Lädt Daten aus einem spezifischen Benutzer"""
        file_path = self.saves_path / "user_data" / user_id / f"{filename}.json"
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.info(f"Loaded user data from {file_path}")
                    return data
            else:
                self.logger.warning(f"File not found: {file_path}")
        except Exception as e:
            self.logger.error(f"Error loading user data from {file_path}: {e}", exc_info=True)
        return []
    
    def get_all_users(self) -> List[str]:
        """Gibt Liste aller User-IDs zurück"""
        user_dir = self.saves_path / "user_data"
        try:
            users = [d.name for d in user_dir.iterdir() if d.is_dir()]
            self.logger.info(f"Found {len(users)} users in {user_dir}")
            return users
        except Exception as e:
            self.logger.error(f"Error getting all users from {user_dir}: {e}", exc_info=True)
        return []