import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import logging
from streamlit_calendar import calendar
from app.klassen.dataLoader import DataLoader
from app.klassen.dataSaver import DataSaver
from app.klassen.kurse import Kurs, Kurstermin
from app.klassen.mitglieder import Mitglied

# Logging zentral initialisieren
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
	logging.basicConfig(
		level=logging.DEBUG,
		format="%(asctime)s %(levelname)s %(name)s: %(message)s"
	)

def get_kurstermine():
	dl = DataLoader()
	kurse = dl.load_all_courses()
	termine = []
	for kurs in kurse:
		kurs_obj = Kurs(**kurs)
		kurs_termine = dl.load_course_dates(kurs_obj.id)
		for termin in kurs_termine:
			if isinstance(termin, dict):
				datum = termin.get("datum")
				uhrzeit = termin.get("uhrzeit")
				termin_obj = Kurstermin(
					id=termin.get("id"),
					kurs=kurs_obj,
					datum=datum,
					uhrzeit=uhrzeit
				)
			else:
				datum = getattr(termin, "datum", None)
				uhrzeit = getattr(termin, "uhrzeit", None)
				termin_obj = termin
			termine.append(
				{
					"title": kurs_obj.name,
					"start": f"{datum}T{str(uhrzeit)}",
					"end": f"{datum}T{str(uhrzeit)}",
					"kurs": kurs_obj,
					"kurstermin": termin_obj,
				}
			)
	logger.debug(f"Kurstermine geladen: {len(termine)} Termine gefunden")
	return termine

def get_user_buchungen():
	buchungen = []
	if st.session_state.mitgliedsnummer:
		dl = DataLoader()
		kurse = dl.load_all_courses()
		user_id = str(st.session_state.mitgliedsnummer)
		
		for kurs in kurse:
			kurs_obj = Kurs(**kurs)
			termine = dl.load_course_dates(kurs_obj.id)
			
			for termin in termine:
				# Handle dict oder object
				if isinstance(termin, dict):
					termin_obj = Kurstermin(
						id=termin.get("id"),
						kurs=kurs_obj,
						datum=termin.get("datum"),
						uhrzeit=termin.get("uhrzeit"),
						kursbuchungen=termin.get("kursbuchungen", [])
					)
				else:
					termin_obj = termin
				
				# Prüfe kursbuchungen
				kursbuchungen = getattr(termin_obj, "kursbuchungen", [])
				if user_id in kursbuchungen:
					buchungen.append({
						"kurs": kurs_obj,
						"kurstermin": termin_obj,
						"datum": getattr(termin_obj, "datum", termin.get("datum") if isinstance(termin, dict) else None),
						"uhrzeit": getattr(termin_obj, "uhrzeit", termin.get("uhrzeit") if isinstance(termin, dict) else None),
					})
	
	logger.info(f"Buchungen für Mitglied {st.session_state.get('mitgliedsnummer')}: {len(buchungen)} gefunden")
	return buchungen

def get_user_trainingsfortschritt():
	fortschritte = []
	if st.session_state.mitgliedsnummer:
		dl = DataLoader()
		fortschritte = dl.load_user_data(
			st.session_state.mitgliedsnummer, "fortschritte"
		)
	logger.debug(f"Trainingsfortschritte geladen für Mitglied {st.session_state.get('mitgliedsnummer')}: {len(fortschritte) if fortschritte else 0}")
	return fortschritte if fortschritte else []

def visualize_user_trainingsfortschritt():
	if st.session_state.mitgliedsnummer:
		fortschritte = get_user_trainingsfortschritt()
		if fortschritte:
			daten = []
			for eintrag in fortschritte:
				if isinstance(eintrag, dict):
					daten.append(
						{
							"Datum": eintrag.get("datum"),
							"Übung": eintrag.get("übung"),
							"Best": eintrag.get("best"),
							"Einheit": eintrag.get("einheit"),
							"Reps": eintrag.get("reps"),
						}
					)
				else:
					daten.append(
						{
							"Datum": getattr(eintrag, "datum", None),
							"Übung": getattr(eintrag, "übung", None),
							"Best": getattr(eintrag, "best", None),
							"Einheit": getattr(eintrag, "einheit", None),
							"Reps": getattr(eintrag, "reps", None),
						}
					)
			df = pd.DataFrame(daten)
			if not df.empty:
				logger.info(f"Visualisiere Trainingsfortschritt für {len(df['Übung'].unique())} Übungen")
				for uebung in df["Übung"].unique():
					df_uebung = df[df["Übung"] == uebung]
					reps_vary = df_uebung["Reps"].nunique() > 1
					if reps_vary:
						col1, col2, col3 = st.columns(3)
						with col1:
							fig1, ax1 = plt.subplots()
							ax1.plot(df_uebung["Datum"], df_uebung["Best"], marker="o", color="blue")
							ax1.set_xlabel("Datum")
							ax1.set_ylabel(df_uebung["Einheit"].iloc[0] if not df_uebung["Einheit"].empty else "Best")
							ax1.set_title(f"{uebung} - Bester Wert")
							st.pyplot(fig1)
						with col2:
							fig2, ax2 = plt.subplots()
							ax2.plot(df_uebung["Datum"], df_uebung["Reps"], marker="o", color="green")
							ax2.set_xlabel("Datum")
							ax2.set_ylabel("Wiederholungen")
							ax2.set_title(f"{uebung} - Wiederholungen")
							st.pyplot(fig2)
						with col3:
							fig3, ax3 = plt.subplots()
							ax3.plot(df_uebung["Datum"], df_uebung["Best"] * df_uebung["Reps"], marker="o", color="orange")
							ax3.set_xlabel("Datum")
							ax3.set_ylabel("Bester Wert x Wiederholungen")
							ax3.set_title(f"{uebung} - Bester Wert x Wiederholungen")
							st.pyplot(fig3)
					else:
						col1, col2, col3 = st.columns(3)
						with col2:
							fig, ax = plt.subplots()
							ax.plot(df_uebung["Datum"], df_uebung["Best"] * df_uebung["Reps"], marker="o")
							ax.set_xlabel("Datum")
							ax.set_ylabel(f"Bester Wert bei {df_uebung['Reps'].iloc[0]} Wiederholungen")
							ax.set_title(f"{uebung}")
							st.pyplot(fig)
			else:
				logger.info("Keine Daten zum Visualisieren verfügbar.")
				st.info("Keine Daten zum Visualisieren verfügbar.")
		else:
			logger.info("Keine Trainingsfortschritte gefunden.")
			st.info("Keine Trainingsfortschritte gefunden.")

def add_trainingsfortschritt_form():
	st.markdown("---")
	st.subheader("Neuen Trainingsfortschritt hinzufügen")
	with st.form("add_fortschritt_form"):
		datum = st.date_input("Datum")
		uebung = st.text_input("Übung")
		best = st.number_input("Bester Wert", min_value=0.0, step=0.1)
		einheit = st.text_input("Einheit (z.B. kg, min)")
		reps = st.number_input("Wiederholungen", min_value=0, step=1)
		submitted = st.form_submit_button("Speichern")
		if submitted:
			new_entry = {
				"datum": str(datum),
				"übung": uebung,
				"best": best,
				"einheit": einheit,
				"reps": reps
			}
			ds = DataSaver()
			dl = DataLoader()
			fortschritte = dl.load_user_data(st.session_state.mitgliedsnummer, "fortschritte")
			if not isinstance(fortschritte, list):
				fortschritte = []
			fortschritte.append(new_entry)
			user_id = str(st.session_state.mitgliedsnummer)
			ds.save_progress(user_id, fortschritte)
			logger.info(f"Neuer Trainingsfortschritt gespeichert für Mitglied {user_id}: {new_entry}")

def show_user():
	st.title("🏃🏻‍♂️ Deer-Fit Mitglied")
	st.write("Willkommen im Mitglieder-Bereich!")

	with st.sidebar:
		st.header("Navigation")
		nav = st.radio(
			"Bereich wählen",
			["Trainingsfortschritt", "Trainingsplan", "Kurse", "Meine Buchungen"],
		)
		st.button("Logout", on_click=lambda: logout())

	if nav == "Trainingsfortschritt":
		st.subheader("Trainingsfortschritt")
		visualize_user_trainingsfortschritt()
		add_trainingsfortschritt_form()

	elif nav == "Trainingsplan":
		st.subheader("Dein Trainingsplan (Empfehlung)")
		dl = DataLoader()
		fortschritte = get_user_trainingsfortschritt()
		userdata = dl.load_user_data(st.session_state.mitgliedsnummer, "user")
		user = Mitglied(userdata.get("vorname", "N/A"), userdata.get("nachname", "N/A"), st.session_state.mitgliedsnummer, fortschritte, userdata.get("mitgliedschaft", {}))
		if fortschritte:
			ziel = st.selectbox(
				"Trainingsziel wählen",
				["Allgemein", "Muskelaufbau", "Abnehmen", "Beweglichkeit"],
			)
			plan = user.trainingsplan_empfehlung(ziel)
			st.markdown("\n".join([f"- {p}" for p in plan]))

	elif nav == "Kurse":
		st.subheader("Kurs-Termine buchen")
		try:
			termine = get_kurstermine()
			logger.debug(f"{len(termine)} Kurstermine für Kalender geladen.")
		except Exception as e:
			logger.error(f"Fehler beim Laden der Kurstermine: {e}", exc_info=True)
			st.error("Fehler beim Laden der Kurstermine.")
			return

		events = [
			{"title": t["title"], "start": t["start"], "end": t["end"]} for t in termine
		]
		try:
			selected = calendar(
				events=events,
				options={"selectable": True, "height": 500, "locale": "de"},
				custom_css=".fc-event {cursor:pointer;}",
			)
			st.info("Klicken Sie auf einen Termin im Kalender, um zu buchen.")
			logger.debug("Kalender erfolgreich angezeigt.")
		except Exception as e:
			logger.error(f"Fehler beim Anzeigen des Kalenders: {e}", exc_info=True)
			st.error("Fehler beim Anzeigen des Kalenders.")
			return

		if selected and selected.get("callback") == "eventClick":
			logger.info(f"Kalender-Event ausgewählt: {selected['eventClick']['event']}")
			st.session_state.selected_event = selected["eventClick"]["event"]
		else:
			logger.debug("Kein Kalender-Event ausgewählt oder Event-Daten fehlen. selected: %s", selected)

		event = st.session_state.get("selected_event", None)
		if event:
			logger.debug(f"Ausgewähltes Event: {event}")
			try:
				sel = next(
					(
						t
						for t in termine
						if t["title"] == event["title"]
						#and t["start"] == event["start"]
					),
					None,
				)
			except Exception as e:
				logger.error(f"Fehler bei der Suche nach passendem Termin: {e}", exc_info=True)
				st.error("Fehler bei der Verarbeitung des ausgewählten Termins.")
				return

			if sel:
				kurs = sel["kurs"]
				logger.info(f"Passenden Kurs gefunden: {kurs.name} (ID: {kurs.id})")
				kurstermin = sel["kurstermin"]
				logger.info(f"Passenden Kurstermin gefunden: {kurstermin.uhrzeit} (ID: {kurstermin.id})")
				try:
					st.markdown(
						f"**{kurs.name}** am {kurstermin.datum} um {kurstermin.uhrzeit}")
				except Exception as e:
					logger.error(f"Fehler beim Anzeigen der Kursdetails: {e}", exc_info=True)
					st.error("Fehler beim Anzeigen der Kursdetails.")
					return

				ds = DataSaver()
				user_id = str(st.session_state.mitgliedsnummer)

				# Prüfe, ob schon gebucht
				try:
					schon_gebucht = user_id in getattr(kurstermin, "kursbuchungen", [])
					logger.info(f"Mitglied {user_id} Buchungsstatus für Termin {getattr(kurstermin, 'id', 'unbekannt')}: {'bereits gebucht' if schon_gebucht else 'noch nicht gebucht'}")
				except Exception as e:
					logger.error(f"Fehler beim Prüfen des Buchungsstatus: {e}", exc_info=True)
					st.error("Fehler beim Prüfen des Buchungsstatus.")
					return

				if schon_gebucht:
					st.info("Sie haben diesen Termin bereits gebucht.")
				else:
					try:
						max_teilnehmer = getattr(kurs, 'max_teilnehmer', 0)
						anzahl_buchungen = len(getattr(kurstermin, 'kursbuchungen', []))
						logger.info(f"Teilnehmerzahl für Kurs {kurs.id}: {anzahl_buchungen}/{max_teilnehmer}")
					except Exception as e:
						logger.error(f"Fehler beim Ermitteln der Teilnehmerzahl: {e}", exc_info=True)
						st.error("Fehler beim Ermitteln der Teilnehmerzahl.")
						return

					try:
						if int(anzahl_buchungen) < int(max_teilnehmer):
							logger.info(f"Mitglied {user_id} versucht, Termin {getattr(kurstermin, 'id', 'unbekannt')} zu buchen. Aktuelle Teilnehmerzahl: {anzahl_buchungen}/{max_teilnehmer}")
							if st.button("Diesen Termin buchen"):
								try:
									kurstermin.teilnehmer_hinzufuegen(user_id)
									ds.save_booking({
										"mitgliedsnummer": user_id,
										"kurs_id": kurs.id,
										"termin_id": kurstermin.id,
									})
									st.success("Erfolgreich gebucht!")
									logger.info(f"Buchung erfolgreich: Mitglied {user_id}, Kurs {kurs.id}, Termin {kurstermin.id}")
									st.session_state.selected_event = None
								except Exception as e:
									logger.error(f"Fehler beim Buchen: {e}", exc_info=True)
									st.error(f"Fehler beim Buchen: {str(e)}")
						else:
							st.warning("Kurs ist voll!")
							logger.warning(f"Kurs {kurs.id} am Termin {kurstermin.id} ist voll.")
					except Exception as e:
						logger.error(f"Fehler beim Vergleich Teilnehmerzahl/max_teilnehmer: {e}", exc_info=True)
					
			else:
				logger.info(f"Kein passender Kurs gefunden für Event: {event}")
		else:
			logger.debug("Kein Event in session_state.selected_event gefunden.")

	elif nav == "Meine Buchungen":
		st.subheader("Meine gebuchten Kurse")
		buchungen = get_user_buchungen()
		if buchungen:
			for b in buchungen:
				st.markdown(f"- **{b['kurs'].name}** am {b['datum']} um {b['uhrzeit']}")
		else:
			st.info("Sie haben noch keine Kurse gebucht.")

def logout():
	st.session_state.logged_in = False
	st.session_state.role = None
	logger.info("User wurde ausgeloggt.")