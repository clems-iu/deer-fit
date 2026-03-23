import uuid
from typing import Optional
import streamlit as st
from app.klassen.abstrakt.jsonFolderRepository import JsonFolderRepository
from app.klassen.abstrakt.jsonListRepository import JsonListRepository
from streamlit_calendar import calendar
from app.klassen.kurse import Kurs, Kurstermin
import logging


logger = logging.getLogger(__name__)


def get_kurseRepo() -> JsonFolderRepository:
    return JsonFolderRepository(
        base_path=f"studio_data/kurse/",
        item_cls=Kurs,
        from_dict=Kurs.from_dict,
        to_dict=Kurs.to_dict,
        details_filename="details.json",
        type="object",
    )


def kurse_section():
    st.markdown('<div class="subtitle">🏋️ Kurse Übersicht</div>', unsafe_allow_html=True)
    kurseRepo = get_kurseRepo()
    kursliste = kurseRepo.list_all()

    if kursliste:
        kurs_cols = st.columns(2)
        for idx, kurs in enumerate(kursliste):
            with kurs_cols[idx % 2]:
                st.markdown(
                    f"<div class='kurs-card'>"
                    f"<b style='color:#2E8B57;'>{kurs.name}</b><br>"
                    f"<span style='font-size:0.95em; color:#2E8B57;'>{kurs.beschreibung}</span><br>"
                    f"<span style='color:#888'>Dauer: {kurs.dauer} min | "
                    f"max {kurs.max_teilnehmer} TN</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    neuer_kurs_form(kurseRepo)


def neuer_kurs_form(repo):
    with st.expander("➕ Neuen Kurs anlegen", expanded=False):
        with st.form("add_course_form"):
            kurs_name = st.text_input("Kursname")
            beschreibung = st.text_area("Beschreibung")
            schwierigkeitsgrad = st.selectbox(
                "Schwierigkeitsgrad", ["Einfach", "Mittel", "Schwer"]
            )
            dauer = st.number_input(
                "Dauer (Minuten)", min_value=1, max_value=300, value=60
            )
            max_teilnehmer = st.number_input(
                "Max. Teilnehmer", min_value=1, max_value=100, value=10
            )
            submitted_kurs = st.form_submit_button("Kurs anlegen")

            if submitted_kurs:
                kurs_data = Kurs(
                    kurs_name, beschreibung, dauer, max_teilnehmer, schwierigkeitsgrad
                )
                if repo.add(kurs_data, str(kurs_data.id)):
                    st.success(f"Kurs {kurs_name} wurde angelegt.")
                else:
                    st.error("Fehler beim Anlegen des Kurses.")


def get_kurstermineRepo(kurs_id: Optional[str] = None) -> JsonFolderRepository:
    if not kurs_id:
        return JsonFolderRepository(
            base_path=f"studio_data/kurse/",
            item_cls=Kurstermin,
            from_dict=Kurstermin.from_dict,
            to_dict=Kurstermin.to_dict,
            details_filename="termine.json",
            type="list",
        )
    else:
        return JsonListRepository(
            path=f"studio_data/kurse/{kurs_id}/termine.json",
            item_cls=Kurstermin,
            from_dict=Kurstermin.from_dict,
            to_dict=Kurstermin.to_dict,
        )


def kalender_section():
    st.markdown(
        '<div class="subtitle">📅 Kurs-Termine Kalender</div>', unsafe_allow_html=True
    )

    kurseRepo = get_kurseRepo()
    kursliste = kurseRepo.list_all()
    
    termineRepo = get_kurstermineRepo()
    termineliste = termineRepo.list_all()
    
    all_events = []
    kurse_by_id = {kurs.id: kurs for kurs in kursliste}
    
    for termin in termineliste:
        kurs = kurse_by_id.get(termin.kursId)
        if kurs is None:
            logger.info(f"Termin {termin.id} verweist auf unbekannten Kurs {termin.kursId}")
            continue  # Überspringt Termine ohne gültigen Kurs
            
        all_events.append(
            {
                "id": f"{termin.kursId}-{termin.id}",
                "title": f"{kurs.name} ({termin.uhrzeit})",
                "start": f"{termin.datum}T{termin.uhrzeit}:00",
                "end": f"{termin.datum}T{termin.uhrzeit}:00",
                "extendedProps": {
                    "kurs_id": termin.kursId,
                    "termin_id": termin.id,
                },
            }
        )

    calendar_options = {
        "initialView": "dayGridMonth",
        "locale": "de",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay",
        },
        "editable": False,
        "selectable": True,
        "height": 600,
    }

    cal_return = calendar(
        events=all_events,
        options=calendar_options,
        custom_css=".fc .fc-toolbar-title { color: #2E8B57; }",
    )

    neuer_termin_form(kursliste)


def neuer_termin_form(kursliste):
    with st.expander("➕ Neuen Kurstermin hinzufügen", expanded=False):
        with st.form("add_termin_form"):
            kurs_names = [str(k.name) for k in kursliste]
            kurs_name = st.selectbox("Kurs", kurs_names)
            datum = st.date_input("Datum", format="YYYY-MM-DD")
            uhrzeit = st.text_input("Uhrzeit (z.B. 18:00)")
            submitted_termin = st.form_submit_button("Termin anlegen")

            if submitted_termin:
                kurs_id = kursliste[kurs_names.index(kurs_name)].id
                terminRepo = get_kurstermineRepo(kurs_id)

                new_termin = Kurstermin(
                    str(datum),
                    uhrzeit,
                    kurs_id,
                )

                if terminRepo.add(new_termin):
                    st.success(
                        f"Termin für Kurs {kurs_id} am {datum} um {uhrzeit} wurde angelegt."
                    )
                else:
                    st.error("Fehler beim Anlegen des Termins.")
