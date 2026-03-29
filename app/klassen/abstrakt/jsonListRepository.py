# Die Klasse JsonListRepository verwaltet eine Liste von T-Objekten in einer einzigen JSON-Datei.

import json
from pathlib import Path
from typing import Type, TypeVar, Generic, List, Callable, Any, Optional

T = TypeVar("T")


class JsonListRepository(Generic[T]):
    def __init__(
        self,
        path: str | Path,
        item_cls: Type[T],
        from_dict: Callable[[dict], T],
        to_dict: Callable[[T], dict],
    ):
        self._path = Path("app/saves/" + str(path))
        self._item_cls = item_cls
        self._from_dict = from_dict
        self._to_dict = to_dict
        self._items: List[T] = []
        self._load()

    # ---------- interne Helfer ----------

    def _load(self) -> None:
        """Lädt die Liste von Items aus der JSON-Datei. Wenn die Datei nicht existiert, wird eine leere Liste erstellt."""
        if not self._path.exists():
            self._items = []
            return
        with self._path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        self._items = [self._from_dict(d) for d in raw]

    def _save(self) -> None:
        """Speichert die aktuelle Liste von Items in der JSON-Datei."""
        data = [self._to_dict(item) for item in self._items]
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ---------- CRUD-Operationen ----------

    def list_all(self) -> List[T]:
        """Gibt alle geladenen Items zurück."""
        return list(self._items)

    def get(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Sucht ein Item, das die Bedingung erfüllt."""
        for item in self._items:
            if predicate(item):
                return item
        return None

    def add(self, item: T) -> T:
        """Fügt ein neues Item hinzu und speichert die Liste. """
        self._items.append(item)
        self._save()
        return item

    def update(
        self, predicate: Callable[[T], bool], updater: Callable[[T], None]
    ) -> Optional[T]:
        """Aktualisiert das erste Element, das predicate(item) == True erfüllt, mit der updater-Funktion und speichert das Resultat."""
        for item in self._items:
            if predicate(item):
                updater(item)
                self._save()
                return item
        return None

    def delete(self, predicate: Callable[[T], bool]) -> bool:
        """Löscht das erste Element, das predicate(item) == True erfüllt."""
        for idx, item in enumerate(self._items):
            if predicate(item):
                del self._items[idx]
                self._save()
                return True
        return False
