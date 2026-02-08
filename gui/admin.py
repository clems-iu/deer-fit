import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show_admin(deer_fit):
	st.markdown("""
		<style>
		.main-title {font-size:2.5em; font-weight:bold; color:#2E8B57; margin-bottom:0.2em;}
		.subtitle {font-size:1.3em; color:#444; margin-top:1.5em; margin-bottom:0.5em;}
		.mitglied-card {background:#f7f7fa; border-radius:10px; padding:1em; margin-bottom:0.7em; box-shadow:0 2px 8px #e0e0e0;}
		.kurs-card {background:#e8f5e9; border-radius:10px; padding:1em; margin-bottom:0.7em; box-shadow:0 2px 8px #d0e0d0;}
		</style>
	""", unsafe_allow_html=True)

	st.markdown('<div class="main-title">🛠️ Deer-Fit Adminbereich</div>', unsafe_allow_html=True)
	st.info("Willkommen im modernen Admin-Bereich! Verwalten Sie Mitglieder, Kurse und mehr.")

	st.markdown('<div class="subtitle">👥 Mitglieder Übersicht</div>', unsafe_allow_html=True)
	if deer_fit:
		cols = st.columns(2)
		for idx, mitglied in enumerate(deer_fit.mitglieder):
			with cols[idx % 2]:
				st.markdown(f"<div class='mitglied-card'>"
							f"<b>{mitglied.vorname} {mitglied.nachname}</b> <span style='color:#888'>(#{mitglied.mitgliedsnummer})</span><br>"
							f"<span style='font-size:0.95em;'>Mitgliedschaft: <b>{mitglied.mitgliedschaft.get('typ','-')}</b> bis {mitglied.mitgliedschaft.get('enddatum','-')}</span>"
							f"</div>", unsafe_allow_html=True)

	st.markdown('<div class="subtitle">📈 Fortschritt aller Mitglieder</div>', unsafe_allow_html=True)
	if deer_fit:
		for mitglied in deer_fit.mitglieder:
			fortschritt = mitglied.trainingsfortschritt
			if fortschritt:
				daten = []
				for eintrag in fortschritt:
					if isinstance(eintrag, dict):
						daten.append({"Datum": eintrag.get("datum"), "Übung": eintrag.get("übung"), "Max": eintrag.get("max")})
					else:
						daten.append({"Datum": getattr(eintrag, "datum", None), "Übung": getattr(eintrag, "übung", None), "Max": getattr(eintrag, "max", None)})
				df = pd.DataFrame(daten)
				if not df.empty:
					st.markdown(f"<b>{mitglied.vorname} {mitglied.nachname}</b>", unsafe_allow_html=True)
					for uebung in df["Übung"].unique():
						st.markdown(f"<span style='color:#2E8B57;font-style:italic;'>{uebung}</span>", unsafe_allow_html=True)
						df_uebung = df[df["Übung"] == uebung]
						fig, ax = plt.subplots()
						ax.plot(df_uebung["Datum"], df_uebung["Max"], marker="o", color="#2E8B57")
						ax.set_xlabel("Datum")
						ax.set_ylabel("Bester Wert")
						ax.set_title(f"Fortschritt: {uebung}")
						ax.grid(True, linestyle=":", alpha=0.5)
						st.pyplot(fig)

	st.markdown('<div class="subtitle">🏋️ Kurse Übersicht</div>', unsafe_allow_html=True)
	if deer_fit:
		kurs_cols = st.columns(2)
		for idx, kurs in enumerate(deer_fit.kurse):
			with kurs_cols[idx % 2]:
				st.markdown(f"<div class='kurs-card'>"
							f"<b>{kurs.name}</b><br>"
							f"<span style='font-size:0.95em;'>{kurs.beschreibung}</span><br>"
							f"<span style='color:#888'>Dauer: {kurs.dauer} min | max {kurs.max_teilnehmer} TN</span>"
							f"</div>", unsafe_allow_html=True)

	st.markdown('<div class="subtitle">💶 Finanzübersicht</div>', unsafe_allow_html=True)
	st.info("Finanzdaten-Integration möglich, sobald Finanzverwaltung angebunden ist.")

	st.markdown("<br>", unsafe_allow_html=True)
	st.button("🚪 Logout", on_click=lambda: logout())

def logout():
	st.session_state.logged_in = False
	st.session_state.role = None
