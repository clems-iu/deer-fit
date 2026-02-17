import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_calendar import calendar

def get_kurstermine(deer_fit):
	termine = []
	for kurs in deer_fit.kurse:
		for termin in getattr(kurs, "offene_termine", []):
			# Kann dict (aus JSON) oder Kurstermin-Objekt sein
			if isinstance(termin, dict):
				datum = termin.get("datum")
				uhrzeit = termin.get("uhrzeit")
			else:
				datum = getattr(termin, "datum", None)
				uhrzeit = getattr(termin, "uhrzeit", None)
			termine.append({
				"title": kurs.name,
				"start": f"{datum}T{str(uhrzeit)}",
				"end": f"{datum}T{str(uhrzeit)}",
				"kurs": kurs,
				"kurstermin": termin
			})
	return termine

def get_user_buchungen(deer_fit):
	buchungen = []
	if deer_fit and deer_fit.user:
		for kurs in deer_fit.kurse:
			for termin in getattr(kurs, "offene_termine", []):
				for buchung in getattr(termin, "kursbuchungen", []):
					if getattr(buchung, "mitglied", None) == deer_fit.user:
						buchungen.append({
							"kurs": kurs,
							"kurstermin": termin,
							"datum": termin.datum,
							"uhrzeit": termin.uhrzeit
						})
	return buchungen

def show_user(deer_fit):
	st.title("👤 Deer-Fit User")
	st.write("Willkommen im User-Bereich!")

	# Layout: Sidebar für Navigation
	with st.sidebar:
		st.header("Navigation")
		nav = st.radio("Bereich wählen", ["Trainingsfortschritt", "Trainingsplan", "Kurse", "Meine Buchungen"])
		st.button("Logout", on_click=lambda: logout())

	if nav == "Trainingsfortschritt":
		st.subheader("Trainingsfortschritt")
		if deer_fit and deer_fit.user:
			fortschritt = deer_fit.user.trainingsfortschritt
			if fortschritt:
				daten = []
				for eintrag in fortschritt:
					if isinstance(eintrag, dict):
						daten.append({"Datum": eintrag.get("datum"), "Übung": eintrag.get("übung"), "Max": eintrag.get("max")})
					else:
						daten.append({"Datum": getattr(eintrag, "datum", None), "Übung": getattr(eintrag, "übung", None), "Max": getattr(eintrag, "max", None)})
				df = pd.DataFrame(daten)
				if not df.empty:
					for uebung in df["Übung"].unique():
						st.markdown(f"**{uebung}**")
						df_uebung = df[df["Übung"] == uebung]
						fig, ax = plt.subplots()
						ax.plot(df_uebung["Datum"], df_uebung["Max"], marker="o")
						ax.set_xlabel("Datum")
						ax.set_ylabel("Bester Wert")
						ax.set_title(f"Fortschritt: {uebung}")
						st.pyplot(fig)
				else:
					st.info("Noch keine Trainingsfortschritte eingetragen.")
		else:
			st.info("Noch keine Trainingsfortschritte eingetragen.")

	elif nav == "Trainingsplan":
		st.subheader("Dein Trainingsplan (Empfehlung)")
		if deer_fit and deer_fit.user:
			ziel = st.selectbox("Trainingsziel wählen", ["Allgemein", "Muskelaufbau", "Abnehmen", "Beweglichkeit"])
			plan = deer_fit.user.trainingsplan_empfehlung(ziel)
			st.markdown("\n".join([f"- {p}" for p in plan]))

	elif nav == "Kurse":
		st.subheader("Kurs-Termine buchen")
		termine = get_kurstermine(deer_fit)
		events = [
			{
				"title": t["title"],
				"start": t["start"],
				"end": t["end"]
			} for t in termine
		]
		selected = calendar(
			events=events,
			options={"selectable": True, "height": 500, "locale": "de"},
			custom_css=".fc-event {cursor:pointer;}"
		)
		st.info("Klicken Sie auf einen Termin im Kalender, um zu buchen.")
		if selected and "event" in selected:
			# Finde das Termin-Objekt
			sel = next((t for t in termine if t["title"] == selected["event"]["title"] and t["start"] == selected["event"]["start"]), None)
			if sel:
				kurs = sel["kurs"]
				kurstermin = sel["kurstermin"]
				st.markdown(f"**{kurs.name}** am {kurstermin.datum} um {kurstermin.uhrzeit}")
				if len(kurstermin.kursbuchungen) < kurs.max_teilnehmer:
					if st.button("Diesen Termin buchen"):
						from klassen.kurse import Kursbuchung
						buchung = Kursbuchung(deer_fit.user, kurs, kurstermin.datum)
						kurstermin.teilnehmer_hinzufuegen(buchung)
						st.success("Erfolgreich gebucht!")
				else:
					st.warning("Kurs ist voll!")

	elif nav == "Meine Buchungen":
		st.subheader("Meine gebuchten Kurse")
		buchungen = get_user_buchungen(deer_fit)
		if buchungen:
			for b in buchungen:
				st.markdown(f"- **{b['kurs'].name}** am {b['datum']} um {b['uhrzeit']}")
		else:
			st.info("Sie haben noch keine Kurse gebucht.")

def logout():
	st.session_state.logged_in = False
	st.session_state.role = None
