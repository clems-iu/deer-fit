import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import logging
from catboost import CatBoostClassifier
import numpy as np
from datetime import datetime
from streamlit_calendar import calendar
from app.klassen.dataLoader import DataLoader
from app.klassen.dataSaver import DataSaver
from app.klassen.kurse import Kurs, Kurstermin
from app.klassen.mitglieder import Mitglied

# Logging zentral initialisieren
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
	logging.basicConfig(
		level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
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
					id=termin.get("id"), kurs=kurs_obj, datum=datum, uhrzeit=uhrzeit
				)
			else:
				datum = getattr(termin, "datum", None)
				uhrzeit = getattr(termin, "uhrzeit", None)
				termin_obj = termin
			termine.append(
				{
					"id": termin_obj.id,
					"title": kurs_obj.name,
					"start": f"{datum}T{str(uhrzeit)}",
					"end": f"{datum}T{str(uhrzeit)}",
					"kurs": kurs_obj,
					"kurstermin": termin_obj,
				}
			)
	logger.debug(f"Kurstermine geladen: {len(termine)} Termine gefunden")
	return termine


# --- Empfehlungssystem mit CatBoost ---
def get_kursempfehlungen():
	"""
	Liefert für jeden Kurstyp eine Kursempfehlung (basierend auf Schwierigkeitstrend der bisherigen Buchungen)
	und gibt den nächsten Termin für diesen Kurs zurück.
	"""
	if not st.session_state.get("mitgliedsnummer"):
		logger.info("get_kursempfehlungen: Keine Mitgliedsnummer in session_state")
		return []

	dl = DataLoader()
	kurse = dl.load_all_courses()
	termine = get_kurstermine()
	buchungen = get_user_buchungen()

	if not buchungen:
		logger.info("get_kursempfehlungen: Keine Buchungen für Mitglied vorhanden")
		return []

	logger.debug(f"get_kursempfehlungen: {len(buchungen)} Buchungen gefunden")

	# Daten für ML aufbereiten
	df_buchungen = []
	for b in buchungen:
		kurs = b["kurs"]
		df_buchungen.append(
			{
				"typ": kurs.typ,
				"schwierigkeit": kurs.schwierigkeitsgrad,
				"datum": b["datum"],
			}
		)

	if not df_buchungen:
		logger.warning("get_kursempfehlungen: Keine Buchungsdaten aufbereitet")
		return []

	df_buchungen = pd.DataFrame(df_buchungen)
	logger.debug(
		f"get_kursempfehlungen: DataFrame erstellt mit {len(df_buchungen)} Einträgen"
	)

	# Schwierigkeit als ordinales Feature
	schwierigkeits_map = {"Einfach": 0, "Mittel": 1, "Schwer": 2}
	df_buchungen["schwierigkeit_num"] = df_buchungen["schwierigkeit"].map(
		schwierigkeits_map
	)

	# Trend pro Typ bestimmen (letzte 3 Buchungen)
	empfehlungen = []
	typen = df_buchungen["typ"].unique()
	logger.debug(f"get_kursempfehlungen: Verarbeite {len(typen)} Kurstypen: {typen}")

	for typ in typen:
		df_typ = df_buchungen[df_buchungen["typ"] == typ].sort_values("datum")
		logger.debug(f"get_kursempfehlungen: Typ '{typ}' hat {len(df_typ)} Buchungen")

		if len(df_typ) < 2:
			logger.debug(
				f"get_kursempfehlungen: Typ '{typ}' übersprungen (weniger als 2 Buchungen)"
			)
			continue

		# CatBoost für Trend (Regression auf Schwierigkeit)
		X = np.arange(len(df_typ)).reshape(-1, 1)
		y = df_typ["schwierigkeit_num"].values
  
		if len(set(y)) < 2:
			logger.debug(f"Typ '{typ}' übersprungen: Target hat nur einen Wert: {set(y)}")
			continue

		model = CatBoostClassifier(
			iterations=10,
			depth=2,
			learning_rate=1,
			loss_function="MultiClass",
			verbose=0,
		)
		model.fit(X, y)

		# Vorhersage für nächste Buchung
		next_idx = np.array([[len(df_typ)]])
		pred = int(model.predict(next_idx)[0][0])
		logger.debug(
			f"get_kursempfehlungen: Typ '{typ}' - vorhergesagte Schwierigkeit: {pred}"
		)

		# Empfohlene Schwierigkeit
		schwierigkeits_empf = [k for k, v in schwierigkeits_map.items() if v == pred]
		if not schwierigkeits_empf:
			logger.warning(
				f"get_kursempfehlungen: Keine Schwierigkeit für Wert {pred} gefunden"
			)
			continue

		schwierigkeits_empf = schwierigkeits_empf[0]
		logger.debug(
			f"get_kursempfehlungen: Typ '{typ}' - empfohlene Schwierigkeit: {schwierigkeits_empf}"
		)

		# Passenden Kurs finden
		passende_kurse = [
			k
			for k in kurse
			if k["typ"] == typ and k["schwierigkeitsgrad"] == schwierigkeits_empf
		]
		if not passende_kurse:
			logger.warning(
				f"get_kursempfehlungen: Keine Kurse gefunden für Typ '{typ}' mit Schwierigkeit '{schwierigkeits_empf}'"
			)
			continue

		kurs_empf = passende_kurse[0]
		logger.debug(
			f"get_kursempfehlungen: Empfohlener Kurs: {kurs_empf.get('name', 'unbekannt')} (ID: {kurs_empf.get('id')})"
		)

		# Nächster Termin ab heute
		heute = datetime.now().date()
		termine_kurs = [t for t in termine if t["kurs"].id == kurs_empf["id"]]
		logger.debug(
			f"get_kursempfehlungen: {len(termine_kurs)} Termine für Kurs {kurs_empf.get('id')} gefunden"
		)

		termine_kurs = sorted(termine_kurs, key=lambda t: t["kurstermin"].datum)
		naechster_termin = None

		for t in termine_kurs:
			try:
				termin_datum = t["kurstermin"].datum
				if isinstance(termin_datum, str):
					termin_datum = datetime.strptime(termin_datum, "%Y-%m-%d").date()
				if termin_datum >= heute:
					naechster_termin = t
					logger.debug(
						f"get_kursempfehlungen: Nächster Termin gefunden: {termin_datum}"
					)
					break
			except Exception as e:
				logger.warning(
					f"get_kursempfehlungen: Fehler beim Verarbeiten von Termin: {e}"
				)
				continue

		if naechster_termin:
			empfehlungen.append(
				{
					"typ": typ,
					"kurs": kurs_empf,
					"termin": naechster_termin["kurstermin"],
					"datum": naechster_termin["kurstermin"].datum,
					"uhrzeit": naechster_termin["kurstermin"].uhrzeit,
				}
			)
			logger.info(
				f"get_kursempfehlungen: Empfehlung erstellt für Typ '{typ}', Kurs '{kurs_empf.get('name')}', Termin {naechster_termin['kurstermin'].datum}"
			)
		else:
			logger.warning(
				f"get_kursempfehlungen: Kein zukünftiger Termin für empfohlenen Kurs '{kurs_empf.get('name')}' gefunden"
			)

	logger.info(
		f"get_kursempfehlungen: Insgesamt {len(empfehlungen)} Empfehlungen erstellt"
	)
	return empfehlungen


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
						kursbuchungen=termin.get("kursbuchungen", []),
					)
				else:
					termin_obj = termin

				# Prüfe kursbuchungen
				kursbuchungen = getattr(termin_obj, "kursbuchungen", [])
				if user_id in kursbuchungen:
					buchungen.append(
						{
							"kurs": kurs_obj,
							"kurstermin": termin_obj,
							"datum": getattr(
								termin_obj,
								"datum",
								(
									termin.get("datum")
									if isinstance(termin, dict)
									else None
								),
							),
							"uhrzeit": getattr(
								termin_obj,
								"uhrzeit",
								(
									termin.get("uhrzeit")
									if isinstance(termin, dict)
									else None
								),
							),
						}
					)

	logger.info(
		f"Buchungen für Mitglied {st.session_state.get('mitgliedsnummer')}: {len(buchungen)} gefunden"
	)
	return buchungen


def get_user_trainingsfortschritt():
	fortschritte = []
	if st.session_state.mitgliedsnummer:
		dl = DataLoader()
		fortschritte = dl.load_user_data(
			st.session_state.mitgliedsnummer, "fortschritte"
		)
	logger.debug(
		f"Trainingsfortschritte geladen für Mitglied {st.session_state.get('mitgliedsnummer')}: {len(fortschritte) if fortschritte else 0}"
	)
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
				logger.info(
					f"Visualisiere Trainingsfortschritt für {len(df['Übung'].unique())} Übungen"
				)
				for uebung in df["Übung"].unique():
					df_uebung = df[df["Übung"] == uebung]
					reps_vary = df_uebung["Reps"].nunique() > 1
					if reps_vary:
						col1, col2, col3 = st.columns(3)
						with col1:
							fig1, ax1 = plt.subplots()
							ax1.plot(
								df_uebung["Datum"],
								df_uebung["Best"],
								marker="o",
								color="blue",
							)
							ax1.set_xlabel("Datum")
							ax1.set_ylabel(
								df_uebung["Einheit"].iloc[0]
								if not df_uebung["Einheit"].empty
								else "Best"
							)
							ax1.set_title(f"{uebung} - Bester Wert")
							st.pyplot(fig1)
						with col2:
							fig2, ax2 = plt.subplots()
							ax2.plot(
								df_uebung["Datum"],
								df_uebung["Reps"],
								marker="o",
								color="green",
							)
							ax2.set_xlabel("Datum")
							ax2.set_ylabel("Wiederholungen")
							ax2.set_title(f"{uebung} - Wiederholungen")
							st.pyplot(fig2)
						with col3:
							fig3, ax3 = plt.subplots()
							ax3.plot(
								df_uebung["Datum"],
								df_uebung["Best"] * df_uebung["Reps"],
								marker="o",
								color="orange",
							)
							ax3.set_xlabel("Datum")
							ax3.set_ylabel("Bester Wert x Wiederholungen")
							ax3.set_title(f"{uebung} - Bester Wert x Wiederholungen")
							st.pyplot(fig3)
					else:
						col1, col2, col3 = st.columns(3)
						with col2:
							fig, ax = plt.subplots()
							ax.plot(
								df_uebung["Datum"],
								df_uebung["Best"] * df_uebung["Reps"],
								marker="o",
							)
							ax.set_xlabel("Datum")
							ax.set_ylabel(
								f"Bester Wert bei {df_uebung['Reps'].iloc[0]} Wiederholungen"
							)
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
				"reps": reps,
			}
			ds = DataSaver()
			dl = DataLoader()
			fortschritte = dl.load_user_data(
				st.session_state.mitgliedsnummer, "fortschritte"
			)
			if not isinstance(fortschritte, list):
				fortschritte = []
			fortschritte.append(new_entry)
			user_id = str(st.session_state.mitgliedsnummer)
			ds.save_progress(user_id, fortschritte)
			logger.info(
				f"Neuer Trainingsfortschritt gespeichert für Mitglied {user_id}: {new_entry}"
			)


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
		user = Mitglied(
			userdata.get("vorname", "N/A"),
			userdata.get("nachname", "N/A"),
			st.session_state.mitgliedsnummer,
			fortschritte,
			userdata.get("mitgliedschaft", {}),
		)
		if fortschritte:
			ziel = st.selectbox(
				"Trainingsziel wählen",
				["Allgemein", "Muskelaufbau", "Abnehmen", "Beweglichkeit"],
			)
			plan = user.trainingsplan_empfehlung(ziel)
			st.markdown("\n".join([f"- {p}" for p in plan]))

	elif nav == "Kurse":
		st.subheader("Kurs-Termine buchen")
		# Empfehlungen anzeigen
		empfehlungen = get_kursempfehlungen()
		if empfehlungen:
			st.markdown("### Persönliche Kurs-Empfehlungen")
			for emp in empfehlungen:
				kurs = emp["kurs"]
				termin = emp["termin"]
				st.markdown(
					f"**{kurs['name']}** ({kurs['typ']}, Schwierigkeit: {kurs['schwierigkeitsgrad']})<br>Nächster Termin: {emp['datum']} um {emp['uhrzeit']}",
					unsafe_allow_html=True,
				)
				# Buchungsbutton direkt für Empfehlung
				ds = DataSaver()
				user_id = str(st.session_state.mitgliedsnummer)
				schon_gebucht = user_id in getattr(termin, "kursbuchungen", [])
				max_teilnehmer = getattr(termin.kurs, "max_teilnehmer", 0)
				anzahl_buchungen = len(getattr(termin, "kursbuchungen", []))
				if schon_gebucht:
					st.info("Sie haben diesen Termin bereits gebucht.")
				elif int(anzahl_buchungen) >= int(max_teilnehmer):
					st.warning("Kurs ist voll!")
				else:
					if st.button(
						f"Empfohlenen Termin buchen: {kurs['name']} {emp['datum']} {emp['uhrzeit']}"
					):
						try:
							termin.teilnehmer_hinzufuegen(user_id)
							ds.save_booking(
								{
									"mitgliedsnummer": user_id,
									"kurs_id": kurs["id"],
									"termin_id": termin.id,
								}
							)
							st.success("Empfohlener Termin erfolgreich gebucht!")
							logger.info(
								f"Empfohlene Buchung erfolgreich: Mitglied {user_id}, Kurs {kurs['id']}, Termin {termin.id}"
							)
						except Exception as e:
							logger.error(
								f"Fehler beim Buchen des empfohlenen Termins: {e}",
								exc_info=True,
							)
							st.error(f"Fehler beim Buchen: {str(e)}")

		# Kalender anzeigen
		try:
			termine = get_kurstermine()
			logger.debug(f"{len(termine)} Kurstermine für Kalender geladen.")
			# Debug-Ausgabe der ersten 25 Termine
			for t in termine[:25]:
				logger.debug(
					f"Termin ID: {t['id']}, Title: {t['title']}, Start: {t['start']}, End: {t['end']}"
				)
		except Exception as e:
			logger.error(f"Fehler beim Laden der Kurstermine: {e}", exc_info=True)
			st.error("Fehler beim Laden der Kurstermine.")
			return

		events = [
			{"id": t["id"], "title": t["title"], "start": t["start"], "end": t["end"]}
			for t in termine
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
			logger.debug(
				"Kein Kalender-Event ausgewählt oder Event-Daten fehlen. selected: %s",
				selected,
			)

		event = st.session_state.get("selected_event", None)
		if event:
			logger.debug(f"Ausgewähltes Event: {event}")
			try:
				sel = next(
					(t for t in termine if str(t["id"]) == str(event["id"])),
					None,
				)
			except Exception as e:
				logger.error(
					f"Fehler bei der Suche nach passendem Termin: {e}", exc_info=True
				)
				st.error("Fehler bei der Verarbeitung des ausgewählten Termins.")
				return

			if sel:
				kurs = sel["kurs"]
				logger.info(f"Passenden Kurs gefunden: {kurs.name} (ID: {kurs.id})")
				kurstermin = sel["kurstermin"]
				logger.info(
					f"Passenden Kurstermin gefunden: {kurstermin.uhrzeit} (ID: {kurstermin.id})"
				)
				try:
					st.markdown(
						f"**{kurs.name}** am {kurstermin.datum} um {kurstermin.uhrzeit}"
					)
				except Exception as e:
					logger.error(
						f"Fehler beim Anzeigen der Kursdetails: {e}", exc_info=True
					)
					st.error("Fehler beim Anzeigen der Kursdetails.")
					return

				ds = DataSaver()
				user_id = str(st.session_state.mitgliedsnummer)

				# Prüfe, ob schon gebucht
				try:
					schon_gebucht = user_id in getattr(kurstermin, "kursbuchungen", [])
					logger.info(
						f"Mitglied {user_id} Buchungsstatus für Termin {getattr(kurstermin, 'id', 'unbekannt')}: {'bereits gebucht' if schon_gebucht else 'noch nicht gebucht'}"
					)
				except Exception as e:
					logger.error(
						f"Fehler beim Prüfen des Buchungsstatus: {e}", exc_info=True
					)
					st.error("Fehler beim Prüfen des Buchungsstatus.")
					return

				if schon_gebucht:
					st.info("Sie haben diesen Termin bereits gebucht.")
				else:
					try:
						max_teilnehmer = getattr(kurs, "max_teilnehmer", 0)
						anzahl_buchungen = len(getattr(kurstermin, "kursbuchungen", []))
						logger.info(
							f"Teilnehmerzahl für Kurs {kurs.id}: {anzahl_buchungen}/{max_teilnehmer}"
						)
					except Exception as e:
						logger.error(
							f"Fehler beim Ermitteln der Teilnehmerzahl: {e}",
							exc_info=True,
						)
						st.error("Fehler beim Ermitteln der Teilnehmerzahl.")
						return

					try:
						if int(anzahl_buchungen) < int(max_teilnehmer):
							logger.info(
								f"Mitglied {user_id} versucht, Termin {getattr(kurstermin, 'id', 'unbekannt')} zu buchen. Aktuelle Teilnehmerzahl: {anzahl_buchungen}/{max_teilnehmer}"
							)
							if st.button("Diesen Termin buchen"):
								try:
									kurstermin.teilnehmer_hinzufuegen(user_id)
									ds.save_booking(
										{
											"mitgliedsnummer": user_id,
											"kurs_id": kurs.id,
											"termin_id": kurstermin.id,
										}
									)
									st.success("Erfolgreich gebucht!")
									logger.info(
										f"Buchung erfolgreich: Mitglied {user_id}, Kurs {kurs.id}, Termin {kurstermin.id}"
									)
									st.session_state.selected_event = None
								except Exception as e:
									logger.error(
										f"Fehler beim Buchen: {e}", exc_info=True
									)
									st.error(f"Fehler beim Buchen: {str(e)}")
						else:
							st.warning("Kurs ist voll!")
							logger.warning(
								f"Kurs {kurs.id} am Termin {kurstermin.id} ist voll."
							)
					except Exception as e:
						logger.error(
							f"Fehler beim Vergleich Teilnehmerzahl/max_teilnehmer: {e}",
							exc_info=True,
						)

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
