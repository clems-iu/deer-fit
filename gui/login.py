import streamlit as st

def show_login():
	st.title("🦌 Deer-Fit Login")
	st.write("Bitte wählen Sie Ihre Rolle und melden Sie sich an.")
	role = st.selectbox("Rolle auswählen", ["user", "admin"])
	username = st.text_input("Benutzername")
	password = st.text_input("Passwort", type="password")
	if st.button("Login"):
		# Dummy-Login, hier kann Authentifizierung ergänzt werden
		if username and password:
			st.session_state.logged_in = True
			st.session_state.role = role
			# DeerFit-Objekt wird in app.py initialisiert
		else:
			st.warning("Bitte Benutzername und Passwort eingeben.")
