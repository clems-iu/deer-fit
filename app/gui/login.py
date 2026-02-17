import streamlit as st
import app.klassen.authenticator as auth

def show_login():
	st.title("🦌 Deer-Fit Login")
	mitgliedsnummer = st.text_input("Mitgliedsnummer")
	password = st.text_input("Passwort", type="password")
	if st.button("Login"):
     
		if mitgliedsnummer and password:
			authenticator = auth.Authenticator()
			authenticator.login(mitgliedsnummer, password)
			if authenticator.authenticated:
				st.session_state.logged_in = True
				st.session_state.role = authenticator.role
				st.session_state.mitgliedsnummer = authenticator.mitgliedsnummer
				st.success(f"Erfolgreich als {authenticator.role} eingeloggt!")
			else:
				st.error("Ungültige Anmeldedaten. Bitte erneut versuchen.")

		else:
			st.warning("Bitte Mitgliedsnummer und Passwort eingeben.")
