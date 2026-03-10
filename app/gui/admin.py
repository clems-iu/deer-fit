import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.klassen.dataLoader import DataLoader
from app.klassen.dataSaver import DataSaver


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
			mitgliedsnummer = st.text_input("Mitgliedsnummer (z.B. 1003)")
			mitgliedschaft_typ = st.selectbox("Mitgliedschafts-Typ", ["Basis", "Premium", "Flexibel"])
			startdatum = st.date_input("Startdatum", format="YYYY-MM-DD")
			enddatum = st.date_input("Enddatum", format="YYYY-MM-DD")
			submitted = st.form_submit_button("Mitglied anlegen")
			if submitted:
				user_data = {
					"vorname": vorname,
					"nachname": nachname,
					"mitgliedsnummer": mitgliedsnummer,
					"mitgliedschaft": {
						"typ": mitgliedschaft_typ,
						"startdatum": str(startdatum),
						"enddatum": str(enddatum)
					}
				}
				if ds.save_user(user_data):
					st.success(f"Mitglied {vorname} {nachname} wurde angelegt.")
				else:
					st.error("Fehler beim Anlegen des Mitglieds.")

	# st.markdown('<div class="subtitle">📈 Fortschritt aller Mitglieder</div>', unsafe_allow_html=True)
	# if deer_fit:
	# 	for mitglied in deer_fit.mitglieder:
	# 		fortschritt = mitglied.trainingsfortschritt
	# 		if fortschritt:
	# 			daten = []
	# 			for eintrag in fortschritt:
	# 				if isinstance(eintrag, dict):
	# 					daten.append({"Datum": eintrag.get("datum"), "Übung": eintrag.get("übung"), "Max": eintrag.get("max")})
	# 				else:
	# 					daten.append({"Datum": getattr(eintrag, "datum", None), "Übung": getattr(eintrag, "übung", None), "Max": getattr(eintrag, "max", None)})
	# 			df = pd.DataFrame(daten)
	# 			if not df.empty:
	# 				st.markdown(f"<b>{mitglied.vorname} {mitglied.nachname}</b>", unsafe_allow_html=True)
	# 				for uebung in df["Übung"].unique():
	# 					st.markdown(f"<span style='color:#2E8B57;font-style:italic;'>{uebung}</span>", unsafe_allow_html=True)
	# 					df_uebung = df[df["Übung"] == uebung]
	# 					fig, ax = plt.subplots()
	# 					ax.plot(df_uebung["Datum"], df_uebung["Max"], marker="o", color="#2E8B57")
	# 					ax.set_xlabel("Datum")
	# 					ax.set_ylabel("Bester Wert")
	# 					ax.set_title(f"Fortschritt: {uebung}")
	# 					ax.grid(True, linestyle=":", alpha=0.5)
	# 					st.pyplot(fig)

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
			kurs_id = st.text_input("Kurs-ID (z.B. 12)")
			kurs_name = st.text_input("Kursname")
			beschreibung = st.text_area("Beschreibung")
			schwierigkeitsgrad = st.selectbox("Schwierigkeitsgrad", ["Einfach", "Mittel", "Schwer"])
			dauer = st.number_input("Dauer (Minuten)", min_value=1, max_value=300, value=60)
			max_teilnehmer = st.number_input("Max. Teilnehmer", min_value=1, max_value=100, value=10)
			submitted_kurs = st.form_submit_button("Kurs anlegen")
			if submitted_kurs:
				kurs_data = {
					"id": kurs_id,
					"name": kurs_name,
					"beschreibung": beschreibung,
					"schwierigkeitsgrad": schwierigkeitsgrad,
					"dauer": dauer,
					"max_teilnehmer": max_teilnehmer
				}
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
						f"<span style='font-size:0.95em;color:#2E8B57'>Anschaffung: <b>{eq.get('anschaffungsjahr','-')}</b> | Kosten: {eq.get('kosten','-')} EUR | Wiederkehrend: {eq.get('sindKostenWiederkehrend', False)}</span>"
						f"</div>", unsafe_allow_html=True)

	with st.expander("➕ Neues Equipment hinzufügen", expanded=False):
		with st.form("add_equipment_form"):
			eq_name = st.text_input("Name")
			eq_jahr = st.number_input("Anschaffungsjahr", min_value=2000, max_value=2100, value=2024)
			eq_kosten = st.number_input("Kosten (EUR)", min_value=0, value=0)
			eq_wiederkehrend = st.checkbox("Kosten wiederkehrend?", value=False)
			submitted_eq = st.form_submit_button("Equipment anlegen")
			if submitted_eq:
				import uuid
				eq_data = {
					"id": str(uuid.uuid4()),
					"name": eq_name,
					"anschaffungsjahr": eq_jahr,
					"kosten": eq_kosten,
					"sindKostenWiederkehrend": eq_wiederkehrend
				}
				if ds.save_equipment(eq_data):
					st.success(f"Equipment {eq_name} wurde angelegt.")
				else:
					st.error("Fehler beim Anlegen des Equipments.")

	# --- Kalender für Kurstermine ---
	st.markdown('<div class="subtitle">📅 Kurs-Termine Kalender</div>', unsafe_allow_html=True)
	from streamlit_calendar import calendar
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
			kurs_ids = [str(k.get('id')) for k in all_courses]
			kurs_id = st.selectbox("Kurs-ID", kurs_ids)
			datum = st.date_input("Datum", format="YYYY-MM-DD")
			uhrzeit = st.text_input("Uhrzeit (z.B. 18:00)")
			submitted_termin = st.form_submit_button("Termin anlegen")
			if submitted_termin:
				# Termin speichern
				# Hole aktuelle Termine
				termine = dl.load_course_dates(kurs_id)
				# Neue ID generieren
				new_id = max([t.get('id', 0) for t in termine], default=0) + 1
				new_termin = {"id": new_id, "datum": str(datum), "uhrzeit": uhrzeit, "kursbuchungen": []}
				termine.append(new_termin)
				# Speichern
				if ds.save_course_dates(kurs_id, termine):
					st.success(f"Termin für Kurs {kurs_id} am {datum} um {uhrzeit} wurde angelegt.")
				else:
					st.error("Fehler beim Anlegen des Termins.")

	st.markdown('<div class="subtitle">💶 Finanzübersicht</div>', unsafe_allow_html=True)
	st.info("Finanzdaten-Integration möglich, sobald Finanzverwaltung angebunden ist.")

	st.markdown("<br>", unsafe_allow_html=True)
	st.button("🚪 Logout", on_click=lambda: logout())

def logout():
	st.session_state.logged_in = False
	st.session_state.role = None
