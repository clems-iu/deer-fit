# Integrationstest für Kursbuchung: Testet den gesamten Ablauf von der Erstellung eines Kurses, über die Buchung eines Kurstermins, bis hin zum Reload der Daten und Überprüfung der Buchung.
# Requirement: Planung und Organisation von Kursen -> Persistenz der Kurs- und Buchungsdaten, Konsistenz der Daten nach Reload

import shutil
from pathlib import Path

from app.klassen.mitglieder import Mitglied
from app.klassen.kurse import Kurs, Kurstermin
from app.klassen.abstrakt.jsonFolderRepository import JsonFolderRepository
from app.klassen.abstrakt.jsonListRepository import JsonListRepository


def test_course_booking_integration():
    # --- Testpfade (isoliert) ---
    base_path = Path("app/saves/test_studio_data")

    if base_path.exists():
        shutil.rmtree(base_path)

    # --- Repositories ---
    kurs_repo = JsonFolderRepository(
        base_path="test_studio_data/kurse/",
        item_cls=Kurs,
        from_dict=Kurs.from_dict,
        to_dict=Kurs.to_dict,
        details_filename="details.json",
        type="object",
    )

    # --- Testdaten: Mitglied ---
    member = Mitglied(
        vorname="Rudy",
        nachname="Rentier",
        trainingsfortschritt=[],
        mitgliedschaft={"typ": "Basis"},
    )
    user_id = str(member.mitgliedsnummer)

    # --- Testdaten: Kurs ---
    kurs = Kurs(
        name="Yoga Basics",
        typ="Yoga",
        schwierigkeitsgrad="Einfach",
        beschreibung="Testkurs",
        dauer=60,
        max_teilnehmer=10,
    )

    kurs_repo.add(kurs, kurs.id)

    # --- Testdaten: Kurstermin ---
    termin = Kurstermin(
        kursId=kurs.id,
        datum="2026-04-01",
        uhrzeit="10:00",
        kursbuchungen=[],
    )

    termin_repo = JsonListRepository(
        path=f"test_studio_data/kurse/{kurs.id}/termine.json",
        item_cls=Kurstermin,
        from_dict=Kurstermin.from_dict,
        to_dict=Kurstermin.to_dict,
    )

    termin_repo.add(termin)

    # --- Aktion: Buchung durchführen ---

    termin_repo.update(
        predicate=lambda t: t.id == termin.id,
        updater=lambda t: setattr(
            t,
            "kursbuchungen",
            getattr(t, "kursbuchungen", []) + [user_id],
        ),
    )

    # --- Reload (Simulation Neustart) ---
    new_repo = JsonListRepository(
        path=f"test_studio_data/kurse/{kurs.id}/termine.json",
        item_cls=Kurstermin,
        from_dict=Kurstermin.from_dict,
        to_dict=Kurstermin.to_dict,
    )

    termine = new_repo.list_all()

    # --- Assertions ---
    assert len(termine) == 1

    loaded_termin = termine[0]
    assert user_id in loaded_termin.kursbuchungen

    # --- Cleanup ---
    shutil.rmtree(base_path)