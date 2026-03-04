import streamlit as st
import app.klassen.authenticator as auth

def show_login():

	# mittlere von 3 Spalten nutzen (1/3 der Fläche)
	col_left, col_center, col_right = st.columns([1, 1, 1])
	with col_center:
		with st.container():
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
						st.rerun()
					else:
						st.error("Ungültige Anmeldedaten. Bitte erneut versuchen.")
				else:
					st.warning("Bitte Mitgliedsnummer und Passwort eingeben.")
