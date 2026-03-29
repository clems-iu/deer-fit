# Visualisiert die Trainingsfortschritte eines Mitglieds und ermöglicht das Hinzufügen neuer Fortschritte.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import logging

from app.klassen.abstrakt.jsonListRepository import JsonListRepository
from app.klassen.mitglieder import Trainingsfortschritt

logger = logging.getLogger(__name__)


def get_fortschritts_repo(mitgliedsnummer: str) -> JsonListRepository:
    return JsonListRepository(
        path=f"user_data/{mitgliedsnummer}/fortschritte.json",
        item_cls=Trainingsfortschritt,
        from_dict=Trainingsfortschritt.from_dict,
        to_dict=Trainingsfortschritt.to_dict,
    )


def load_trainingsfortschritte(mitgliedsnummer: str):
    repo = get_fortschritts_repo(mitgliedsnummer)
    return repo.list_all()


def normalize_fortschritte(fortschritte):
    """Normalisiert die Trainingsfortschritte in ein DataFrame, unabhängig davon, ob sie als dicts oder Objekte vorliegen."""
    daten = []
    for eintrag in fortschritte:
        if isinstance(eintrag, dict):
            daten.append(
                {
                    "Datum": eintrag.get("datum"),
                    "Übung": eintrag.get("übung"),
                    "Best": eintrag.get("best"),
                    "Einheit": eintrag.get("einheit"),
                    "Reps": eintrag.get("reps"),
                }
            )
        else:
            daten.append(
                {
                    "Datum": getattr(eintrag, "datum", None),
                    "Übung": getattr(eintrag, "übung", None),
                    "Best": getattr(eintrag, "best", None),
                    "Einheit": getattr(eintrag, "einheit", None),
                    "Reps": getattr(eintrag, "reps", None),
                }
            )
    return pd.DataFrame(daten)


def visualize_user_trainingsfortschritt(mitgliedsnummer: str):
    """Lädt die Trainingsfortschritte eines Mitglieds, normalisiert die Daten und visualisiert sie mit Matplotlib."""
    fortschritte = load_trainingsfortschritte(mitgliedsnummer)

    if not fortschritte:
        st.info("Keine Trainingsfortschritte gefunden.")
        logger.info("Keine Trainingsfortschritte gefunden.")
        return

    df = normalize_fortschritte(fortschritte)

    if df.empty:
        st.info("Keine Daten zum Visualisieren verfügbar.")
        logger.info("Keine Daten zum Visualisieren verfügbar.")
        return

    logger.info(
        f"Visualisiere Trainingsfortschritt für {len(df['Übung'].unique())} Übungen"
    )

    for uebung in df["Übung"].dropna().unique():
        df_uebung = df[df["Übung"] == uebung].copy()
        reps_vary = df_uebung["Reps"].nunique() > 1

        if reps_vary:
            col1, col2, col3 = st.columns(3)

            with col1:
                fig1, ax1 = plt.subplots()
                ax1.plot(
                    df_uebung["Datum"], df_uebung["Best"], marker="o", color="blue"
                )
                ax1.set_xlabel("Datum")
                ax1.set_ylabel(
                    df_uebung["Einheit"].iloc[0]
                    if not df_uebung["Einheit"].empty
                    else "Best"
                )
                ax1.set_title(f"{uebung} - Bester Wert")
                st.pyplot(fig1)
                plt.close(fig1)

            with col2:
                fig2, ax2 = plt.subplots()
                ax2.plot(
                    df_uebung["Datum"], df_uebung["Reps"], marker="o", color="green"
                )
                ax2.set_xlabel("Datum")
                ax2.set_ylabel("Wiederholungen")
                ax2.set_title(f"{uebung} - Wiederholungen")
                st.pyplot(fig2)
                plt.close(fig2)

            with col3:
                fig3, ax3 = plt.subplots()
                ax3.plot(
                    df_uebung["Datum"],
                    df_uebung["Best"] * df_uebung["Reps"],
                    marker="o",
                    color="orange",
                )
                ax3.set_xlabel("Datum")
                ax3.set_ylabel("Bester Wert x Wiederholungen")
                ax3.set_title(f"{uebung} - Bester Wert x Wiederholungen")
                st.pyplot(fig3)
                plt.close(fig3)
        else:
            col1, col2, col3 = st.columns(3)
            with col2:
                fig, ax = plt.subplots()
                ax.plot(
                    df_uebung["Datum"],
                    df_uebung["Best"] * df_uebung["Reps"],
                    marker="o",
                )
                ax.set_xlabel("Datum")
                ax.set_ylabel(
                    f"Bester Wert bei {df_uebung['Reps'].iloc[0]} Wiederholungen"
                )
                ax.set_title(str(uebung))
                st.pyplot(fig)
                plt.close(fig)


def add_trainingsfortschritt_form(mitgliedsnummer: str):
    """Zeigt ein Formular zum Hinzufügen eines neuen Trainingsfortschritts an und speichert die Daten im Repository."""
    
    st.markdown("---")
    st.subheader("Neuen Trainingsfortschritt hinzufügen")

    with st.form("add_fortschritt_form"):
        datum = st.date_input("Datum")
        uebung = st.text_input("Übung")
        best = st.number_input("Bester Wert", min_value=0.0, step=0.1)
        einheit = st.text_input("Einheit (z.B. kg, min)")
        reps = st.number_input("Wiederholungen", min_value=0, step=1)
        submitted = st.form_submit_button("Speichern")

    if submitted:
        repo = get_fortschritts_repo(mitgliedsnummer)
        new_entry = Trainingsfortschritt(str(datum), uebung, best, einheit, reps)
        repo.add(new_entry)
        logger.info(
            f"Neuer Trainingsfortschritt gespeichert für Mitglied {mitgliedsnummer}: {new_entry}"
        )
        st.success("Trainingsfortschritt gespeichert.")


def show_trainingsfortschritt():
    """Hauptfunktion, die den Trainingsfortschritt anzeigt und das Formular zum Hinzufügen neuer Fortschritte bereitstellt."""
    
    st.subheader("Trainingsfortschritt")

    mitgliedsnummer = st.session_state.get("mitgliedsnummer")
    if not mitgliedsnummer:
        logger.warning(
            "Mitgliedsnummer nicht gefunden. Kann Trainingsfortschritt nicht anzeigen."
        )
        st.warning("Mitgliedsnummer nicht gefunden. Bitte logge dich erneut ein.")
        return

    visualize_user_trainingsfortschritt(mitgliedsnummer)
    add_trainingsfortschritt_form(mitgliedsnummer)
