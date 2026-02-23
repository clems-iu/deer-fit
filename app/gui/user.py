import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_calendar import calendar
from app.klassen.dataLoader import DataLoader
from app.klassen.kurse import Kurs
from app.klassen.mitglieder import Mitglied

def get_kurstermine():
    dl = DataLoader()
    kurse = dl.load_all_courses()
    termine = []
    for kurs in kurse:
        kurs_obj = Kurs(**kurs)
        kurs_termine = dl.load_course_dates(kurs_obj.id)  # <-- Name geändert!
        for termin in kurs_termine:
            # Kann dict (aus JSON) oder Kurstermin-Objekt sein
            if isinstance(termin, dict):
                datum = termin.get("datum")
                uhrzeit = termin.get("uhrzeit")
            else:
                datum = getattr(termin, "datum", None)
                uhrzeit = getattr(termin, "uhrzeit", None)
            termine.append(
                {
                    "title": kurs_obj.name,
                    "start": f"{datum}T{str(uhrzeit)}",
                    "end": f"{datum}T{str(uhrzeit)}",
                    "kurs": kurs_obj,
                    "kurstermin": termin,
                }
            )
    return termine


def get_user_buchungen():
	buchungen = []
	if st.session_state.mitgliedsnummer:
		dl = DataLoader()
		kurse = dl.load_all_courses()
		for kurs in kurse:
			kurs_obj = Kurs(**kurs)
			termine = dl.load_course_dates(kurs_obj.id)
			for termin in termine:
				for buchung in getattr(termin, "kursbuchungen", []):
					if (
						getattr(buchung, "mitgliedsnummer", None)
						== st.session_state.mitgliedsnummer
					):
						buchungen.append(
							{
								"kurs": kurs,
								"kurstermin": termin,
								"datum": termin.datum,
								"uhrzeit": termin.uhrzeit,
							}
						)
	return buchungen

def get_user_trainingsfortschritt():
	fortschritte = []
	if st.session_state.mitgliedsnummer:
		dl = DataLoader()
		fortschritte = dl.load_user_data(
			st.session_state.mitgliedsnummer, "fortschritte"
		)
	return fortschritte

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
				for uebung in df["Übung"].unique():
					st.markdown(f"**{uebung}**")
					df_uebung = df[df["Übung"] == uebung]
					fig, ax = plt.subplots()
					ax.plot(df_uebung["Datum"], df_uebung["Best"], marker="o")
					ax.set_xlabel("Datum")
					ax.set_ylabel("Bester Wert")
					ax.set_title(f"Fortschritt: {uebung}")
					st.pyplot(fig)
			else:
				st.info("Keine Daten zum Visualisieren verfügbar.")
		else:
			st.info("Keine Trainingsfortschritte gefunden.")


def show_user():
	st.title("👤 Deer-Fit User")
	st.write("Willkommen im User-Bereich!")

	# Layout: Sidebar für Navigation
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
		termine = get_kurstermine()
		events = [
			{"title": t["title"], "start": t["start"], "end": t["end"]} for t in termine
		]
		selected = calendar(
			events=events,
			options={"selectable": True, "height": 500, "locale": "de"},
			custom_css=".fc-event {cursor:pointer;}",
		)
		st.info("Klicken Sie auf einen Termin im Kalender, um zu buchen.")
		if selected and "event" in selected:
			# Finde das Termin-Objekt
			sel = next(
				(
					t
					for t in termine
					if t["title"] == selected["event"]["title"]
					and t["start"] == selected["event"]["start"]
				),
				None,
			)
			if sel:
				kurs = sel["kurs"]
				kurstermin = sel["kurstermin"]
				st.markdown(
					f"**{kurs.name}** am {kurstermin.datum} um {kurstermin.uhrzeit}"
				)
				if len(kurstermin.kursbuchungen) < kurs.max_teilnehmer:
					if st.button("Diesen Termin buchen"):
				
						kurstermin.teilnehmer_hinzufuegen(st.session_state.mitgliedsnummer)
						st.success("Erfolgreich gebucht!")
				else:
					st.warning("Kurs ist voll!")

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
