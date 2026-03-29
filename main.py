# Hier  wird das Logging initialisiert und die Hauptfunktion der Streamlit-App definiert. 
# Je nach Anmeldestatus und Rolle des Benutzers wird die entsprechende Ansicht (Login, Admin oder User) angezeigt.

import streamlit as st
import logging

from config.logging_config import setup_logging
from app.gui.user_view import user
from app.gui.admin_view import admin
from app.gui.login_view import login




def main():
    st.set_page_config(page_title="Deer-Fit", page_icon="🦌", layout="wide")
    
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("System gestartet")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.mitgliedsnummer = None
        
    if not st.session_state.logged_in:
        login.show_login()    
    else:
        if st.session_state.role == 'admin':
            admin.show_admin()
        elif st.session_state.role == 'user':
            user.show_user()
        else:
            st.error("Ungültige Rolle. Bitte neu anmelden.")

if __name__ == "__main__":
    main()