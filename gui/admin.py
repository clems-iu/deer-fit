import streamlit as st


def show_admin(deer_fit):
	st.title("🛠️ Deer-Fit Admin")
	st.write("Willkommen im Admin-Bereich!")
	st.subheader("Mitglieder Übersicht:")
	if deer_fit:
		for mitglied in deer_fit.mitglieder:
			st.markdown(f"**{mitglied.vorname} {mitglied.nachname}** (#{mitglied.mitgliedsnummer}) - {mitglied.mitgliedschaft}")
	st.subheader("Kurse Übersicht:")
	if deer_fit:
		for kurs in deer_fit.kurse:
			st.markdown(f"**{kurs.name}**: {kurs.beschreibung} ({kurs.dauer} min, max {kurs.max_teilnehmer} TN)")
	st.button("Logout", on_click=lambda: logout())

def logout():
	st.session_state.logged_in = False
	st.session_state.role = None
