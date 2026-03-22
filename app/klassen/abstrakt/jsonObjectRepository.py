import json
from pathlib import Path
from typing import Type, TypeVar, Generic, Callable, Optional

T = TypeVar("T")

class JsonObjectRepository(Generic[T]):
    def __init__(
        self,
        path: str | Path,
        item_cls: Type[T],
        from_dict: Callable[[dict], T],
        to_dict: Callable[[T], dict],
    ):
        self._path = Path(path)
        self._item_cls = item_cls
        self._from_dict = from_dict
        self._to_dict = to_dict
        self._item: Optional[T] = None
        self._load()

    # ---------- intern ----------

    def _load(self) -> None:
        if not self._path.exists():
            self._item = None
            return
        with self._path.open("r", encoding="utf-8") as f:
            raw = json.load(f)          # erwartet ein Dict
        self._item = self._from_dict(raw)

    def _save(self) -> None:
        if self._item is None:
            # falls du in dem Fall lieber eine leere Datei oder gar nichts schreiben willst,
            # kannst du das hier anpassen
            self._path.unlink(missing_ok=True)
            return
        data = self._to_dict(self._item)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ---------- CRUD-artige Operationen ----------

    def get(self) -> Optional[T]:
        """Gibt das aktuell gespeicherte Objekt zurück (oder None)."""
        return self._item

    def set(self, item: T) -> T:
        """Ersetzt das Objekt durch `item` und speichert es."""
        self._item = item
        self._save()
        return item

    def update(self, updater: Callable[[T], None]) -> Optional[T]:
        """
        Ruft `updater` mit dem aktuellen Objekt auf, speichert danach.
        Falls noch kein Objekt vorhanden ist, passiert nichts.
        """
        if self._item is None:
            return None
        updater(self._item)
        self._save()
        return self._item

    def delete(self) -> None:
        """Löscht das Objekt (und optional die Datei)."""
        self._item = None
        self._save()
