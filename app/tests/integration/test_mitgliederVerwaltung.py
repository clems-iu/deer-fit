# Integrationstest für Mitgliederverwaltung: Testet den gesamten Ablauf von der Erstellung eines Mitglieds, über das Speichern und Laden der Daten, bis hin zur Überprüfung der Konsistenz der Daten nach einem Reload.
# Requirement: Verwaltung von Mitgliedschaften -> Persistenz der Mitgliedsdaten, Konsistenz der Daten nach Reload

import shutil
from pathlib import Path

from app.klassen.mitglieder import Mitglied
from app.klassen.abstrakt.jsonFolderRepository import JsonFolderRepository


def test_create_member_persistence():
    # --- Testpfad vorbereiten (isoliert) ---
    test_base_path = Path("app/saves/test_user_data")

    # Falls alter Testmüll existiert → löschen
    if test_base_path.exists():
        shutil.rmtree(test_base_path)

    # Repository erstellen
    repo = JsonFolderRepository(
        base_path="test_user_data/",
        item_cls=Mitglied,
        from_dict=Mitglied.from_dict,
        to_dict=Mitglied.to_dict,
        details_filename="user.json",
        type="object",
    )

    # --- Testdaten ---
    mitglied = Mitglied(
        vorname="Rudy",
        nachname="Rentier",
        trainingsfortschritt=[],
        mitgliedschaft={
            "typ": "Premium",
            "startdatum": "2026-01-01",
            "enddatum": "2026-12-31",
        },
    )

    # --- Aktion: Mitglied speichern ---
    repo.add(mitglied, str(mitglied.mitgliedsnummer))

    # --- Neue Instanz simuliert "Neustart" ---
    new_repo = JsonFolderRepository(
        base_path="test_user_data/",
        item_cls=Mitglied,
        from_dict=Mitglied.from_dict,
        to_dict=Mitglied.to_dict,
        details_filename="user.json",
        type="object",
    )

    members = new_repo.list_all()

    # --- Assertions ---
    assert len(members) == 1

    loaded_member = members[0]
    assert loaded_member.vorname == "Rudy"
    assert loaded_member.nachname == "Rentier"
    assert loaded_member.mitgliedschaft["typ"] == "Premium"

    # --- Cleanup ---
    shutil.rmtree(test_base_path)