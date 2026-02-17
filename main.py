#Initialisiert das Deer-Fit Anwendungsmodul.
# Hier werden Daten gespeichert und die Hauptlogik des Programms verwaltet.

# Kursplan nur eine Darstellung der Kurstermine als Dictionary für die einfache Handhabung in der App über das GUI
# Kurse sind der Ankerpunkt der Systemlogik für Mitglieder
# Von eingeloggten Mitglied aus werden Aktionen ausgeführt wie Kursbuchungen, Trainingsfortschritte hinzufügen etc.
# Dieses wird auch als Filter zur Anzeige der relevanten Daten genutzt


# Streamlit App: Login und Weiterleitung
import streamlit as st
from app.gui import login, user, admin


def main():
    st.set_page_config(page_title="Deer-Fit Login", page_icon="🦌", layout="centered")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.mitgliedsnummer = None
        
    if not st.session_state.logged_in:
        login.show_login()    
    else:
        if st.session_state.role == 'admin':
            admin.show_admin(st.session_state.deer_fit)
        elif st.session_state.role == 'user':
            user.show_user(st.session_state.deer_fit)
        else:
            st.error("Ungültige Rolle. Bitte neu anmelden.")

if __name__ == "__main__":
    main()