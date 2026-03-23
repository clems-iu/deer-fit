import streamlit as st
from app.klassen.mitglieder import Mitglied
from app.klassen.abstrakt.jsonFolderRepository import JsonFolderRepository


def get_mitgliederRepo():
    return JsonFolderRepository(
        base_path=f"user_data/",
        item_cls=Mitglied,
        from_dict=Mitglied.from_dict,
        to_dict=Mitglied.to_dict,
        details_filename="user.json",
        type="object",
    )


def mitglieder_section():
    st.markdown(
        '<div class="subtitle">👥 Mitglieder Übersicht</div>', unsafe_allow_html=True
    )
    mitglieder_repo = get_mitgliederRepo()
    userliste = mitglieder_repo.list_all()

    if userliste:
        cols = st.columns(2)
        for idx, mitglied in enumerate(userliste):
            with cols[idx % 2]:
                st.markdown(
                    f"<div class='mitglied-card'>"
                    f"<b style='color:#2E8B57;'>{mitglied.vorname} {mitglied.nachname}</b> "
                    f"<span style='color:#888'>(#{mitglied.mitgliedsnummer})</span><br>"
                    f"<span style='font-size:0.95em;color:#2E8B57'>Mitgliedschaft: "
                    f"<b>{mitglied.mitgliedschaft.get('typ','-')}</b> "
                    f"bis {mitglied.mitgliedschaft.get('enddatum','-')}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    neues_mitglied_form(mitglieder_repo)


def neues_mitglied_form(repo):
    with st.expander("➕ Neues Mitglied anlegen", expanded=False):
        with st.form("add_user_form"):
            vorname = st.text_input("Vorname")
            nachname = st.text_input("Nachname")
            mitgliedschaft_typ = st.selectbox(
                "Mitgliedschafts-Typ", ["Basis", "Premium", "Flexibel"]
            )
            startdatum = st.date_input("Startdatum", format="YYYY-MM-DD")
            enddatum = st.date_input("Enddatum", format="YYYY-MM-DD")
            submitted = st.form_submit_button("Mitglied anlegen")

            if submitted:
                user_data = Mitglied(
                    vorname,
                    nachname,
                    [],
                    {
                        "typ": mitgliedschaft_typ,
                        "startdatum": str(startdatum),
                        "enddatum": str(enddatum),
                    },
                )
                if repo.add(user_data, str(user_data.mitgliedsnummer)):
                    st.success(f"Mitglied {vorname} {nachname} wurde angelegt.")
                    st.rerun()
                else:
                    st.error("Fehler beim Anlegen des Mitglieds.")
