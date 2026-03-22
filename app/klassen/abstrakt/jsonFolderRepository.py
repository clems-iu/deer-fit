import json
from pathlib import Path
from typing import Type, TypeVar, Generic, List, Callable, Any, Optional

T = TypeVar("T")


class JsonFolderRepository(Generic[T]):
    """
    Erwartete Struktur:

    base_path/
      folder1/
        details.json
      folder2/
        details.json
      ...

    Die Klasse erzeugt eine Liste von T-Objekten, indem sie in jedem
    Unterordner die angegebene JSON-Datei (z.B. 'details.json') lädt.
    """

    def __init__(
        self,
        base_path: str | Path,
        item_cls: Type[T],
        from_dict: Callable[[dict], T],
        to_dict: Callable[[T], dict],
        details_filename: str = "details.json",
        type: str = "list",
    ):
        self._base_path = Path("app/saves/" + str(base_path))
        self._item_cls = item_cls
        self._from_dict = from_dict
        self._to_dict = to_dict
        self._details_filename = details_filename
        self._items: List[T] = []
        self.type = type  # "list" oder "object"
        self._load()

    # ---------- interne Helfer ----------

    def _iter_detail_files(self) -> List[Path]:
        """
        Sammelt alle 'details.json'-Dateien in den direkten Unterordnern
        von base_path.
        """
        if not self._base_path.exists():
            return []

        detail_files: List[Path] = []
        for child in self._base_path.iterdir():
            if child.is_dir():
                details_path = child / self._details_filename
                if details_path.exists() and details_path.is_file():
                    detail_files.append(details_path)
        return detail_files

    def _load(self) -> None:
        self._items = []
        detail_files = self._iter_detail_files()
        for file_path in detail_files:
            with file_path.open("r", encoding="utf-8") as f:
                if self.type == "list":
                    raw_list = json.load(f)
                    for raw in raw_list:
                        item = self._from_dict(raw)
                        self._items.append(item)
                else:
                    raw = json.load(f)
                    item = self._from_dict(raw)
                    self._items.append(item)

    # ---------- CRUD-Operationen im Speicher ----------

    def list_all(self) -> List[T]:
        return list(self._items)

    def get(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None

    def add(self, item: T, folder_name: str) -> T:
        self._items.append(item)
        # Erstellt Ordner aus folder_name und speichert in details_filename
        folder_path = self._base_path / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        details_path = folder_path / self._details_filename
        with details_path.open("w", encoding="utf-8") as f:
            json.dump(self._to_dict(item), f, ensure_ascii=False, indent=2)
        return item

    def delete(self, predicate: Callable[[T], bool], folder_name: str) -> bool:
        for idx, item in enumerate(self._items):
            if predicate(item):
                del self._items[idx]
                # Optional: Ordner löschen, wenn du möchtest
                folder_path = self._base_path / folder_name
                if folder_path.exists() and folder_path.is_dir():
                    for child in folder_path.iterdir():
                        child.unlink()  # Löscht alle Dateien im Ordner
                    folder_path.rmdir()  # Löscht den Ordner selbst
                return True
        return False
