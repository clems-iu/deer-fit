import streamlit as st
from app.klassen.authenticator import Authenticator

def name_to_id(name: str) -> str:
		# Name in Bytes (UTF-8)
		b = name.encode("utf-8")
		# Bytes als große Zahl interpretieren
		return str(int.from_bytes(b, byteorder="big"))

def id_to_name(member_id: int) -> str:
	# Minimale Byte-Länge bestimmen
	length = (member_id.bit_length() + 7) // 8
	b = member_id.to_bytes(length, byteorder="big")
	return b.decode("utf-8")
	
def show_login():

	# mittlere von 3 Spalten nutzen (1/3 der Fläche)
	col_left, col_center, col_right = st.columns([1, 1, 1])
	with col_center:
		with st.container():
			st.title("🦌 Deer-Fit Login")
			name = st.text_input("Name")
			password = st.text_input("Passwort", type="password")

			if st.button("Login"):
				if name and password:
					if name == "admin" and password == "admin":
						mitgliedsnummer = "admin"
					else:
						mitgliedsnummer = name_to_id(name)
					auth = Authenticator()
					auth.login(mitgliedsnummer, password)
					if auth.authenticated:
						st.session_state.logged_in = True
						st.session_state.role = auth.role
						st.session_state.mitgliedsnummer = auth.mitgliedsnummer
						st.success(f"Erfolgreich als {auth.role} eingeloggt!")
						st.rerun()
					else:
						st.error("Ungültige Anmeldedaten. Bitte erneut versuchen.")
				else:
					st.warning("Bitte Name und Passwort eingeben.")
