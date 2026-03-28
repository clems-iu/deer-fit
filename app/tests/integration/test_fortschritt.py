# Integrationstest für Trainingsfortschritt: Testet den gesamten Ablauf von der Erstellung eines Trainingsfortschritts, über das Speichern und Laden der Daten, bis hin zur Überprüfung der Konsistenz der Daten nach einem Reload.
# Requirement: Tracking von Trainingsfortschritten -> Persistenz der Fortschrittsdaten, Konsistenz der Daten nach Reload

import shutil
from pathlib import Path

from app.klassen.mitglieder import Trainingsfortschritt
from app.klassen.abstrakt.jsonListRepository import JsonListRepository


def test_training_progress_persistence():
    # --- Testpfad vorbereiten ---
    base_path = Path("app/saves/test_user_data_progress")

    if base_path.exists():
        shutil.rmtree(base_path)

    mitgliedsnummer = "9999"

    repo = JsonListRepository(
        path=f"test_user_data_progress/{mitgliedsnummer}/fortschritte.json",
        item_cls=Trainingsfortschritt,
        from_dict=Trainingsfortschritt.from_dict,
        to_dict=Trainingsfortschritt.to_dict,
    )

    # --- Testdaten ---
    eintrag1 = Trainingsfortschritt(
        datum="2026-03-01",
        übung="Bankdrücken",
        best=80.0,
        einheit="kg",
        reps=8,
    )

    eintrag2 = Trainingsfortschritt(
        datum="2026-03-10",
        übung="Bankdrücken",
        best=85.0,
        einheit="kg",
        reps=8,
    )

    # --- Aktion: Fortschritt speichern ---
    repo.add(eintrag1)
    repo.add(eintrag2)

    # --- Reload (Simulation Neustart) ---
    new_repo = JsonListRepository(
        path=f"test_user_data_progress/{mitgliedsnummer}/fortschritte.json",
        item_cls=Trainingsfortschritt,
        from_dict=Trainingsfortschritt.from_dict,
        to_dict=Trainingsfortschritt.to_dict,
    )

    fortschritte = new_repo.list_all()

    # --- Assertions ---
    assert len(fortschritte) == 2

    assert fortschritte[0].best == 80.0
    assert fortschritte[1].best == 85.0

    assert fortschritte[0].übung == "Bankdrücken"
    assert fortschritte[1].übung == "Bankdrücken"

    # Reihenfolge wichtig für Visualisierung
    assert fortschritte[0].datum == "2026-03-01"
    assert fortschritte[1].datum == "2026-03-10"

    # --- Cleanup ---
    shutil.rmtree(base_path)