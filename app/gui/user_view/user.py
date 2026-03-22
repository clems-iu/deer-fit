import logging
import streamlit as st

from app.gui.user_view import trainingsfortschritt
from app.gui.user_view import kursbuchung

import logging

logger = logging.getLogger(__name__)


def show_user():
    st.title("🏃🏻‍♂️ Deer-Fit Mitglied")
    st.write("Willkommen im Mitglieder-Bereich!")

    with st.sidebar:
        st.header("Navigation")
        nav = st.radio(
            "Bereich wählen",
            ["Trainingsfortschritt", "Kurse"],
        )
        st.button("Logout", on_click=lambda: logout())

    if nav == "Trainingsfortschritt":
        trainingsfortschritt.show_trainingsfortschritt()

    elif nav == "Kurse":
        kursbuchung.show_kursbuchungen()


def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    logger.info("User wurde ausgeloggt.")
