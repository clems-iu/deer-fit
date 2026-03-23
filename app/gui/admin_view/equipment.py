import uuid
import streamlit as st

from app.klassen.abstrakt.jsonListRepository import JsonListRepository
from app.klassen.equipment import Equipment

def get_equipmentRepo():
    return JsonListRepository(
        path="studio_data/equipment.json",
        item_cls=Equipment,
        from_dict=Equipment.from_dict,
        to_dict=Equipment.to_dict,
    )

def equipment_section():
    st.markdown('<div class="subtitle">🛠️ Equipment Übersicht</div>', unsafe_allow_html=True)
    equipmentRepo = get_equipmentRepo()
    equipment_liste = equipmentRepo.list_all()

    if equipment_liste:
        for eq in equipment_liste:
            st.markdown(
                f"<div class='mitglied-card'>"
                f"<b style='color:#2E8B57;'>{eq.name}</b> "
                f"<span style='color:#888'>(#{eq.id})</span><br>"
                f"<span style='font-size:0.95em;color:#2E8B57'>Anschaffung: "
                f"<b>{eq.anschaffungsdatum}</b> | "
                f"Kosten: {eq.kosten} EUR | "
                f"Wiederkehrend: {eq.sindKostenWiederkehrend}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

    neues_equipment_form(equipmentRepo)


def neues_equipment_form(repo):
    with st.expander("➕ Neues Equipment hinzufügen", expanded=False):
        with st.form("add_equipment_form"):
            eq_name = st.text_input("Name")
            eq_datum = st.date_input("Anschaffungsdatum", format="YYYY-MM-DD")
            eq_kosten = st.number_input("Kosten (EUR)", min_value=0, value=0)
            eq_wiederkehrend = st.checkbox("Kosten wiederkehrend?", value=False)
            submitted_eq = st.form_submit_button("Equipment anlegen")

            if submitted_eq:
                eq_data = Equipment(
                    name=eq_name,
                    anschaffungsdatum=str(eq_datum),
                    kosten=eq_kosten,
                    sindKostenWiederkehrend=eq_wiederkehrend
                )
                if repo.add(eq_data):
                    st.success(f"Equipment {eq_name} wurde angelegt.")
                else:
                    st.error("Fehler beim Anlegen des Equipments.")
