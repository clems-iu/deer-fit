import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import uuid
from streamlit_calendar import calendar
from app.klassen.intern.dataLoader import DataLoader
from app.klassen.intern.dataSaver import DataSaver
from app.klassen.mitglieder import Mitglied
from app.klassen.kurse import Kurs, Kurstermin


def show_admin():
	dl = DataLoader()
	ds = DataSaver()
	
	st.markdown("""
		<style>
		.main-title {font-size:2.5em; font-weight:bold; color:#2E8B57; margin-bottom:0.2em;}
		.subtitle {font-size:1.3em; color:#444; margin-top:1.5em; margin-bottom:0.5em;}
		.mitglied-card {background:#f7f7fa; border-radius:10px; padding:1em; margin-bottom:0.7em; box-shadow:0 2px 8px #e0e0e0;}
		.kurs-card {background:#e8f5e9; border-radius:10px; padding:1em; margin-bottom:0.7em; box-shadow:0 2px 8px #d0e0d0;}
		</style>
	""", unsafe_allow_html=True)

	st.markdown('<div class="main-title">🛠️ Deer-Fit Adminbereich</div>', unsafe_allow_html=True)
	st.info("Willkommen im Admin-Bereich! Verwalten Sie Mitglieder, Kurse und mehr.")

	st.markdown('<div class="subtitle">👥 Mitglieder Übersicht</div>', unsafe_allow_html=True)
	userliste = dl.get_all_users()
	if userliste:
		cols = st.columns(2)
		for idx, mitglied in enumerate(userliste):
			with cols[idx % 2]:
				st.markdown(f"<div class='mitglied-card'>"
							f"<b style='color:#2E8B57;'>{mitglied.vorname} {mitglied.nachname}</b> <span style='color:#888'>(#{mitglied.mitgliedsnummer})</span><br>"
							f"<span style='font-size:0.95em;color:#2E8B57'>Mitgliedschaft: <b>{mitglied.mitgliedschaft.get('typ','-')}</b> bis {mitglied.mitgliedschaft.get('enddatum','-')}</span>"
							f"</div>", unsafe_allow_html=True)

	# --- Neues Mitglied anlegen ---
	with st.expander("➕ Neues Mitglied anlegen", expanded=False):
		with st.form("add_user_form"):
			vorname = st.text_input("Vorname")
			nachname = st.text_input("Nachname")
			mitgliedschaft_typ = st.selectbox("Mitgliedschafts-Typ", ["Basis", "Premium", "Flexibel"])
			startdatum = st.date_input("Startdatum", format="YYYY-MM-DD")
			enddatum = st.date_input("Enddatum", format="YYYY-MM-DD")
			submitted = st.form_submit_button("Mitglied anlegen")
			if submitted:
				user_data = Mitglied(
					vorname,
					nachname,
					[],
					{
						"typ": mitgliedschaft_typ,
						"startdatum": str(startdatum),
						"enddatum": str(enddatum)
					}
				)
				if ds.save_user(user_data):
					st.success(f"Mitglied {vorname} {nachname} wurde angelegt.")
				else:
					st.error("Fehler beim Anlegen des Mitglieds.")


	st.markdown('<div class="subtitle">🏋️ Kurse Übersicht</div>', unsafe_allow_html=True)
	kursliste = dl.load_all_courses()
	if kursliste:
		kurs_cols = st.columns(2)
		for idx, kurs in enumerate(kursliste):
			with kurs_cols[idx % 2]:
				st.markdown(f"<div class='kurs-card'>"
							f"<b style='color:#2E8B57;'>{kurs.get('name')}</b><br>"
							f"<span style='font-size:0.95em; color:#2E8B57;''>{kurs.get('beschreibung')}</span><br>"
							f"<span style='color:#888'>Dauer: {kurs.get('dauer')} min | max {kurs.get('max_teilnehmer')} TN</span>"
							f"</div>", unsafe_allow_html=True)

	# --- Neuen Kurs anlegen ---
	with st.expander("➕ Neuen Kurs anlegen", expanded=False):
		with st.form("add_course_form"):
			kurs_name = st.text_input("Kursname")
			beschreibung = st.text_area("Beschreibung")
			schwierigkeitsgrad = st.selectbox("Schwierigkeitsgrad", ["Einfach", "Mittel", "Schwer"])
			dauer = st.number_input("Dauer (Minuten)", min_value=1, max_value=300, value=60)
			max_teilnehmer = st.number_input("Max. Teilnehmer", min_value=1, max_value=100, value=10)
			submitted_kurs = st.form_submit_button("Kurs anlegen")
			if submitted_kurs:
				kurs_data = Kurs(kurs_name, beschreibung, dauer, max_teilnehmer, schwierigkeitsgrad)
				if ds.save_course(kurs_data):
					st.success(f"Kurs {kurs_name} wurde angelegt.")
				else:
					st.error("Fehler beim Anlegen des Kurses.")


	# --- Equipment Übersicht & Hinzufügen ---
	st.markdown('<div class="subtitle">🛠️ Equipment Übersicht</div>', unsafe_allow_html=True)
	equipment_liste = dl.load_equipment()
	if equipment_liste:
		for eq in equipment_liste:
			st.markdown(f"<div class='mitglied-card'>"
						f"<b style='color:#2E8B57;'>{eq.get('name')}</b> <span style='color:#888'>(#{eq.get('id','-')})</span><br>"
						f"<span style='font-size:0.95em;color:#2E8B57'>Anschaffung: <b>{eq.get('anschaffungsdatum','-')}</b> | Kosten: {eq.get('kosten','-')} EUR | Wiederkehrend: {eq.get('sindKostenWiederkehrend', False)}</span>"
						f"</div>", unsafe_allow_html=True)

	with st.expander("➕ Neues Equipment hinzufügen", expanded=False):
		with st.form("add_equipment_form"):
			eq_name = st.text_input("Name")
			eq_datum = st.date_input("Anschaffungsdatum", format="YYYY-MM-DD")
			eq_kosten = st.number_input("Kosten (EUR)", min_value=0, value=0)
			eq_wiederkehrend = st.checkbox("Kosten wiederkehrend?", value=False)
			submitted_eq = st.form_submit_button("Equipment anlegen")
			if submitted_eq:
				eq_data = {
					"id": str(uuid.uuid4()),
					"name": eq_name,
					"anschaffungsdatum": str(eq_datum),
					"kosten": eq_kosten,
					"sindKostenWiederkehrend": eq_wiederkehrend
				}
				if ds.save_equipment(eq_data):
					st.success(f"Equipment {eq_name} wurde angelegt.")
				else:
					st.error("Fehler beim Anlegen des Equipments.")

	# --- Kalender für Kurstermine ---
	st.markdown('<div class="subtitle">📅 Kurs-Termine Kalender</div>', unsafe_allow_html=True)
	
	# Alle Termine aus allen Kursen sammeln
	all_courses = dl.load_all_courses()
	all_events = []
	for kurs in all_courses:
		termine = dl.load_course_dates(str(kurs.get('id')))
		for termin in termine:
			all_events.append({
				"id": f"{kurs.get('id')}-{termin.get('id')}",
				"title": f"{kurs.get('name')} ({termin.get('uhrzeit')})",
				"start": f"{termin.get('datum')}T{termin.get('uhrzeit')}:00",
				"end": f"{termin.get('datum')}T{termin.get('uhrzeit')}:00",
				"extendedProps": {"kurs_id": kurs.get('id'), "termin_id": termin.get('id')}
			})

	calendar_options = {
		"initialView": "dayGridMonth",
		"locale": "de",
		"headerToolbar": {"left": "prev,next today", "center": "title", "right": "dayGridMonth,timeGridWeek,timeGridDay"},
		"editable": False,
		"selectable": True,
		"height": 600
	}
	cal_return = calendar(
		events=all_events,
		options=calendar_options,
		custom_css=".fc .fc-toolbar-title { color: #2E8B57; }"
	)

	with st.expander("➕ Neuen Kurstermin hinzufügen", expanded=False):
		with st.form("add_termin_form"):
			kurs_names = [str(k.get('name')) for k in all_courses]
			kurs_name = st.selectbox("Kurs", kurs_names)
			datum = st.date_input("Datum", format="YYYY-MM-DD")
			uhrzeit = st.text_input("Uhrzeit (z.B. 18:00)")
			submitted_termin = st.form_submit_button("Termin anlegen")
			if submitted_termin:
				# Termin speichern
				# Hole aktuelle Termine
				kurs_id = all_courses[kurs_names.index(kurs_name)].get('id')
				termine = dl.load_course_dates(kurs_id)
				# Neue ID generieren
				new_id = str(uuid.uuid4())
				new_termin = {"id": new_id, "datum": str(datum), "uhrzeit": uhrzeit, "kursbuchungen": []}
				termine.append(new_termin)
				# Speichern
				if ds.save_course_dates(kurs_id, termine):
					st.success(f"Termin für Kurs {kurs_id} am {datum} um {uhrzeit} wurde angelegt.")
				else:
					st.error("Fehler beim Anlegen des Termins.")


	# --- Kostenübersicht ---
	
	st.markdown('<div class="subtitle">💶 Kostenübersicht (Monat)</div>', unsafe_allow_html=True)
	# Aktueller Monat und Jahr
	heute = datetime.date.today()
	aktueller_monat = heute.month
	aktuelles_jahr = heute.year

	# Equipment-Kosten berechnen
	equipment_liste = dl.load_equipment()
	kosten_summe = 0
	kosten_zeilen = []
	for eq in equipment_liste:
		anschaffungsdatum_str = eq.get('anschaffungsdatum', '')
		try:
			anschaffungsdatum = datetime.datetime.strptime(str(anschaffungsdatum_str), '%Y-%m-%d').date()
			anschaffungsjahr = anschaffungsdatum.year
			anschaffungsmonat = anschaffungsdatum.month
		except Exception:
			anschaffungsjahr = 0
			anschaffungsmonat = 0
		kosten = float(eq.get('kosten', 0))
		wiederkehrend = eq.get('sindKostenWiederkehrend', False)
		# Kosten zählen, wenn wiederkehrend oder im aktuellen Monat angeschafft
		if wiederkehrend or (anschaffungsjahr == aktuelles_jahr and anschaffungsmonat == aktueller_monat):
			kosten_summe += kosten
			kosten_zeilen.append({
				'name': eq.get('name', '-'),
				'kosten': kosten
			})

	# Einkünfte durch Mitgliedsbeiträge berechnen
	userliste = dl.get_all_users()
	einkuenfte_summe = 0
	einkunft_zeilen = []
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
		# Mitgliedschaft im aktuellen Monat aktiv?
		if start_dt <= heute <= ende_dt:
			if typ == 'Basis':
				beitrag = 20
			elif typ == 'Premium':
				beitrag = 35
			else:
				beitrag = 0
			einkuenfte_summe += beitrag
			einkunft_zeilen.append({
				'name': f"{mitglied.vorname} {mitglied.nachname}",
				'beitrag': beitrag
			})

	# Tabelle anzeigen
	
	kosten_df = pd.DataFrame(kosten_zeilen)
	eink_df = pd.DataFrame(einkunft_zeilen)
	max_len = max(len(kosten_df), len(eink_df))
	# Padding für gleichlange Tabellen
	kosten_df = kosten_df.reindex(range(max_len)).fillna('')
	eink_df = eink_df.reindex(range(max_len)).fillna('')
	# Kombinierte Tabelle
	table = pd.DataFrame({
		'Kosten': kosten_df['name'],
		'Betrag (€)': kosten_df['kosten'],
		'Einkünfte': eink_df['name'],
		'Beitrag (€)': eink_df['beitrag']
	})
	st.table(table)
	# Resultatszeile
	st.markdown(f"**Gesamtkosten:** {kosten_summe:.2f} € | **Gesamteinkünfte:** {einkuenfte_summe:.2f} € | **Ergebnis:** {einkuenfte_summe - kosten_summe:.2f} €")

	st.markdown("<br>", unsafe_allow_html=True)
	st.button("🚪 Logout", on_click=lambda: logout())

def logout():
	st.session_state.logged_in = False
	st.session_state.role = None
