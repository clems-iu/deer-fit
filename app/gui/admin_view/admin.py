# Admin-Bereich für die Verwaltung von Mitgliedern, Kursen, Equipment und Finanzen

import streamlit as st
from .mitglieder import mitglieder_section
from .kurse import kurse_section, kalender_section
from .equipment import equipment_section
from .finanzen import finanzen_section


def show_admin():
    """Zeigt den Admin-Bereich mit Navigation zwischen verschiedenen Verwaltungssektionen."""

    st.markdown(
        """
		<style>
		.main-title {font-size:2.5em; font-weight:bold; color:#2E8B57; margin-bottom:0.2em;}
		.subtitle {font-size:1.3em; color:#444; margin-top:1.5em; margin-bottom:0.5em;}
		.mitglied-card {background:#f7f7fa; border-radius:10px; padding:1em; margin-bottom:0.7em; box-shadow:0 2px 8px #e0e0e0;}
		.kurs-card {background:#e8f5e9; border-radius:10px; padding:1em; margin-bottom:0.7em; box-shadow:0 2px 8px #d0e0d0;}
		</style>
	""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-title">🛠️ Deer-Fit Adminbereich</div>', unsafe_allow_html=True
    )

    st.info(
        "Willkommen im Admin-Bereich! Verwalten Sie hier Mitglieder, Kurse und mehr."
    )

    with st.sidebar:
        st.header("Navigation")
        nav = st.radio(
            "Bereich wählen",
            ["Mitglieder", "Kurse", "Equipment", "Kalender", "Finanzen"],
        )
        st.button("Logout", on_click=lambda: logout())

    if nav == "Mitglieder":
        mitglieder_section()
    elif nav == "Kurse":
        kurse_section()
    elif nav == "Equipment":
        equipment_section()
    elif nav == "Kalender":
        kalender_section()
    elif nav == "Finanzen":
        finanzen_section()


def logout():
    """Setzt den Login-Status zurück und loggt den Benutzer aus."""
    st.session_state.logged_in = False
    st.session_state.role = None
