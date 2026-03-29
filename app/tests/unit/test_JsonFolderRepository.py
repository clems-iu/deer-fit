# Unit-Tests für die zentrale Verwaltung durch die JsonFolderRepository-Klasse

import unittest
import shutil
import json
from pathlib import Path

from app.klassen.abstrakt.jsonFolderRepository import JsonFolderRepository


# Dummy-Klasse für Testzwecke
class DummyItem:
	def __init__(self, name: str):
		self.name = name

	def __eq__(self, other):
		return isinstance(other, DummyItem) and self.name == other.name


def from_dict(data: dict) -> DummyItem:
	return DummyItem(name=data["name"])


def to_dict(item: DummyItem) -> dict:
	return {"name": item.name}


class TestJsonFolderRepository(unittest.TestCase):
	def setUp(self):
		"""Vor jedem Test: Testverzeichnis anlegen und sicherstellen, dass es leer ist."""
		self.base_path = Path("test_repo")
		self.full_path = Path("app/saves") / self.base_path

		if self.full_path.exists():
			shutil.rmtree(self.full_path)

		self.full_path.mkdir(parents=True)

	def tearDown(self):
		"""Nach jedem Test: Testverzeichnis löschen."""
		if self.full_path.exists():
			shutil.rmtree(self.full_path)

	def _create_folder_with_json(self, folder, data):
		"""Hilfsmethode, um einen Ordner mit einer details.json-Datei zu erstellen."""
		folder_path = self.full_path / folder
		folder_path.mkdir(parents=True, exist_ok=True)
		with (folder_path / "details.json").open("w", encoding="utf-8") as f:
			json.dump(data, f)

	# ---------- Tests ----------

	def test_load_list_type(self):
		"""Testet das Laden von Daten, wenn der Typ 'list' ist."""
		self._create_folder_with_json("f1", [{"name": "A"}, {"name": "B"}])

		repo = JsonFolderRepository(
			base_path=self.base_path,
			item_cls=DummyItem,
			from_dict=from_dict,
			to_dict=to_dict,
			type="list",
		)

		items = repo.list_all()
		self.assertEqual(len(items), 2)
		self.assertIn(DummyItem("A"), items)
		self.assertIn(DummyItem("B"), items)

	def test_load_object_type(self):
		"""Testet das Laden von Daten, wenn der Typ 'object' ist."""
		self._create_folder_with_json("f1", {"name": "Single"})

		repo = JsonFolderRepository(
			base_path=self.base_path,
			item_cls=DummyItem,
			from_dict=from_dict,
			to_dict=to_dict,
			type="object",
		)

		items = repo.list_all()
		self.assertEqual(len(items), 1)
		self.assertEqual(items[0], DummyItem("Single"))

	def test_iter_detail_files_empty(self):
		"""Testet die Iteration über detail.json-Dateien, wenn keine vorhanden sind."""
		repo = JsonFolderRepository(
			base_path="non_existing",
			item_cls=DummyItem,
			from_dict=from_dict,
			to_dict=to_dict,
		)
		self.assertEqual(repo.list_all(), [])

	def test_get_found(self):
		"""Testet das Abrufen eines spezifischen vorhandenen Elements."""
		self._create_folder_with_json("f1", [{"name": "X"}])

		repo = JsonFolderRepository(
			base_path=self.base_path,
			item_cls=DummyItem,
			from_dict=from_dict,
			to_dict=to_dict,
		)

		item = repo.get(lambda x: x.name == "X")
		self.assertEqual(item, DummyItem("X"))

	def test_get_not_found(self):
		"""Testet das Abrufen eines spezifischen nicht vorhandenen Elements."""
		repo = JsonFolderRepository(
			base_path=self.base_path,
			item_cls=DummyItem,
			from_dict=from_dict,
			to_dict=to_dict,
		)

		self.assertIsNone(repo.get(lambda x: x.name == "does_not_exist"))

	def test_add_creates_file(self):
		"""Testet das Hinzufügen eines neuen Elements und die Erstellung der entsprechenden details.json-Datei."""
		repo = JsonFolderRepository(
			base_path=self.base_path,
			item_cls=DummyItem,
			from_dict=from_dict,
			to_dict=to_dict,
		)

		item = DummyItem("NewItem")
		repo.add(item, "folder_new")

		file_path = self.full_path / "folder_new" / "details.json"
		self.assertTrue(file_path.exists())

		with file_path.open() as f:
			data = json.load(f)

		self.assertEqual(data["name"], "NewItem")

	def test_delete_existing(self):
		"""Testet das Löschen eines vorhandenen Elements und die Entfernung der entsprechenden details.json-Datei."""
		self._create_folder_with_json("f1", [{"name": "DeleteMe"}])

		repo = JsonFolderRepository(
			base_path=self.base_path,
			item_cls=DummyItem,
			from_dict=from_dict,
			to_dict=to_dict,
		)

		result = repo.delete(lambda x: x.name == "DeleteMe", "f1")

		self.assertTrue(result)
		self.assertEqual(repo.list_all(), [])
		self.assertFalse((self.full_path / "f1").exists())

	def test_delete_not_existing(self):
		"""Testet das Löschen eines nicht vorhandenen Elements, was zu keinem Fehler führen sollte."""
		repo = JsonFolderRepository(
			base_path=self.base_path,
			item_cls=DummyItem,
			from_dict=from_dict,
			to_dict=to_dict,
		)

		result = repo.delete(lambda x: True, "no_folder")
		self.assertFalse(result)


if __name__ == "__main__":
	unittest.main()
