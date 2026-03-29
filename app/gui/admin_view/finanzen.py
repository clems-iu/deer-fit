# Finanzen-Übersicht für den aktuellen Monat

import calendar
import datetime
import pandas as pd
import streamlit as st

from app.klassen.abstrakt.jsonFolderRepository import JsonFolderRepository
from app.klassen.abstrakt.jsonListRepository import JsonListRepository
from app.klassen.equipment import Equipment
from app.klassen.mitglieder import Mitglied

def get_equipmentRepo():
    return JsonListRepository(
        path="studio_data/equipment.json",
        item_cls=Equipment,
        from_dict=Equipment.from_dict,
        to_dict=Equipment.to_dict,
    )
    
def get_mitgliederRepo():
    return JsonFolderRepository(
        base_path=f"user_data/",
        item_cls=Mitglied,
        from_dict=Mitglied.from_dict,
        to_dict=Mitglied.to_dict,
        details_filename="user.json",
        type="object",
    )

def finanzen_section():
    """Zeigt die Kosten- und Einkünfteübersicht für den aktuellen Monat an."""
    st.markdown('<div class="subtitle">💶 Kostenübersicht (Monat)</div>', unsafe_allow_html=True)

    heute = datetime.date.today()
    aktueller_monat = heute.month
    aktuelles_jahr = heute.year

    # Auswertung der Kosten
    equipmentRepo = get_equipmentRepo()
    equipment_liste = equipmentRepo.list_all()
    kosten_summe = 0
    kosten_zeilen = []

    for eq in equipment_liste:
        anschaffungsdatum_str = eq.anschaffungsdatum
        try:
            anschaffungsdatum = datetime.datetime.strptime(str(anschaffungsdatum_str), '%Y-%m-%d').date()
            anschaffungsjahr = anschaffungsdatum.year
            anschaffungsmonat = anschaffungsdatum.month
        except Exception:
            anschaffungsjahr = 0
            anschaffungsmonat = 0

        kosten = float(eq.kosten)
        wiederkehrend = eq.sindKostenWiederkehrend

        if wiederkehrend or (anschaffungsjahr == aktuelles_jahr and anschaffungsmonat == aktueller_monat):
            kosten_summe += kosten
            kosten_zeilen.append({
                'name': eq.name,
                'kosten': kosten
            })

    # Auswertung der Einkünfte
    mitgliederRepo= get_mitgliederRepo()
    userliste = mitgliederRepo.list_all()
    einkuenfte_summe = 0
    einkunft_zeilen = []

    heute = datetime.date.today()

    first_of_month = heute.replace(day=1)
    last_day = calendar.monthrange(heute.year, heute.month)[1]
    last_of_month = heute.replace(day=last_day)

    for mitglied in userliste:
        mitgliedschaft = mitglied.mitgliedschaft
        typ = mitgliedschaft.get('typ', '')
        start = mitgliedschaft.get('startdatum', '')
        ende = mitgliedschaft.get('enddatum', '')

        try:
            start_dt = datetime.datetime.strptime(start, '%Y-%m-%d').date()
            ende_dt = datetime.datetime.strptime(ende, '%Y-%m-%d').date()
        except Exception:
            continue

        if start_dt <= last_of_month and ende_dt >= first_of_month:
            if typ == 'Basis':
                beitrag = 20
            elif typ == 'Premium':
                beitrag = 35
            elif typ == 'Flexibel':
                beitrag = 50
            else:
                beitrag = 0

            einkuenfte_summe += beitrag
            einkunft_zeilen.append({
                'name': f"{mitglied.vorname} {mitglied.nachname}",
                'beitrag': beitrag
            })

    # Darstellung der Tabelle der Kosten und Einkünfte
    
    kosten_df = pd.DataFrame(kosten_zeilen)
    eink_df = pd.DataFrame(einkunft_zeilen)
    max_len = max(len(kosten_df), len(eink_df)) if max(len(kosten_df), len(eink_df)) > 0 else 0

    kosten_df = kosten_df.reindex(range(max_len)).fillna('')
    eink_df = eink_df.reindex(range(max_len)).fillna('')

    table = pd.DataFrame({
        'Kosten': kosten_df['name'],
        'Betrag (€)': kosten_df['kosten'],
        'Einkünfte': eink_df['name'],
        'Beitrag (€)': eink_df['beitrag']
    })

    st.table(table)
    st.markdown(
        f"**Gesamtkosten:** {kosten_summe:.2f} € | "
        f"**Gesamteinkünfte:** {einkuenfte_summe:.2f} € | "
        f"**Ergebnis:** {einkuenfte_summe - kosten_summe:.2f} €"
    )
