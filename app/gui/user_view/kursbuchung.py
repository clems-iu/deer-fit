# Unter diesem Modul werden die Funktionen für die Kursbuchung und das Empfehlungssystem implementiert.
# Es werden die Kurstermine geladen, die Buchungen des Nutzers ermittelt und basierend auf den bisherigen Buchungen personalisierte Empfehlungen generiert.
# Außerdem wird ein Kalender mit den verfügbaren Terminen angezeigt, in dem der Nutzer direkt buchen kann.

import logging
from typing import Optional

import streamlit as st
import pandas as pd
from app.klassen.abstrakt.jsonFolderRepository import JsonFolderRepository
from app.klassen.abstrakt.jsonListRepository import JsonListRepository
from streamlit_calendar import calendar
from catboost import CatBoostClassifier
import numpy as np
from datetime import datetime

from app.klassen.kurse import Kurs, Kurstermin

logger = logging.getLogger(__name__)


def get_kurseRepo() -> JsonFolderRepository:
    return JsonFolderRepository(
        base_path=f"studio_data/kurse/",
        item_cls=Kurs,
        from_dict=Kurs.from_dict,
        to_dict=Kurs.to_dict,
        details_filename="details.json",
        type="object",
    )


def get_kurstermineRepo(kurs_id: Optional[str] = None) -> JsonFolderRepository:
    """Wenn kein kurs_id übergeben wird, werden alle Kurstermine aus allen Kursen geladen.
    Wenn eine kurs_id übergeben wird, werden nur die Kurstermine für diesen Kurs geladen.
    """
    
    if not kurs_id:
        return JsonFolderRepository(
            base_path=f"studio_data/kurse/",
            item_cls=Kurstermin,
            from_dict=Kurstermin.from_dict,
            to_dict=Kurstermin.to_dict,
            details_filename="termine.json",
            type="list",
        )
    else:
        return JsonListRepository(
            path=f"studio_data/kurse/{kurs_id}/termine.json",
            item_cls=Kurstermin,
            from_dict=Kurstermin.from_dict,
            to_dict=Kurstermin.to_dict,
        )


def get_all_kurstermine():
    """Lädt alle Kurstermine aus allen Kursen und ergänzt sie um den optionalen Parameter kurs"""
    termine_repo = get_kurstermineRepo()
    termine = termine_repo.list_all()
    kurs_repo = get_kurseRepo()
    kurs_repos = kurs_repo.list_all()
    
    # Ergänzung der Termine um den optionalen Parameter kurs
    for termin in termine:
        try:
            kurs_id = getattr(termin, "kursId", None)
            if kurs_id:
                passender_kurs = [k for k in kurs_repos if k.id == kurs_id]
                if passender_kurs:
                    termin.kurs = passender_kurs[0]
                    logger.debug(
                        f"Kurs zu Termin {termin.id} zugeordnet: {termin.kurs.name}"
                    )
                else:
                    logger.warning(
                        f"Kein passender Kurs gefunden für Termin {termin.id} mit kursId {kurs_id}"
                    )
            else:
                logger.warning(f"Termin {termin.id} hat keine kursId.")
        except Exception as e:
            logger.error(
                f"Fehler bei der Zuordnung des Kurses für Termin {getattr(termin, 'id', 'unbekannt')}: {e}",
                exc_info=True,
            )
    logger.debug(f"Kurstermine geladen: {len(termine)} Termine gefunden")
    return termine


def get_user_buchungen():
    """Lädt alle Kurstermine, prüft die Kursbuchungen und gibt eine Liste der gebuchten Termine für das aktuelle Mitglied zurück."""
    
    buchungen = []
    if st.session_state.mitgliedsnummer:
        kurse_repo = get_kurseRepo()
        kurse = kurse_repo.list_all()
        mitgliedsnummer = str(st.session_state.mitgliedsnummer)

        for kurs in kurse:
            termine_repo = get_kurstermineRepo(kurs.id)
            termine = termine_repo.list_all()

            for termin in termine:

                # Prüfe kursbuchungen
                kursbuchungen = getattr(termin, "kursbuchungen", [])
                if mitgliedsnummer in kursbuchungen:
                    buchungen.append(
                        {
                            "kurs": kurs,
                            "kurstermin": termin,
                            "datum": termin.datum,
                            "uhrzeit": termin.uhrzeit,
                        }
                    )

    logger.info(
        f"Buchungen für Mitglied {st.session_state.get('mitgliedsnummer')}: {len(buchungen)} gefunden"
    )
    return buchungen


# --- Empfehlungssystem mit CatBoost ---
def get_kursempfehlungen():
    """
    Liefert für jeden Kurstyp eine Kursempfehlung (basierend auf Schwierigkeitstrend der bisherigen Buchungen)
    und gibt den nächsten Termin für diesen Kurs zurück.
    """
    if not st.session_state.get("mitgliedsnummer"):
        logger.info("get_kursempfehlungen: Keine Mitgliedsnummer in session_state")
        return []

    kurse_repo = get_kurseRepo()
    kurse = kurse_repo.list_all()
    termine = get_all_kurstermine()
    buchungen = get_user_buchungen()

    if not buchungen:
        logger.info("get_kursempfehlungen: Keine Buchungen für Mitglied vorhanden")
        return []

    logger.debug(f"get_kursempfehlungen: {len(buchungen)} Buchungen gefunden")

    # Daten für ML aufbereiten
    df_buchungen = []
    for b in buchungen:
        kurs = b["kurs"]
        df_buchungen.append(
            {
                "typ": kurs.typ,
                "schwierigkeit": kurs.schwierigkeitsgrad,
                "datum": b["datum"],
            }
        )

    if not df_buchungen:
        logger.warning("get_kursempfehlungen: Keine Buchungsdaten aufbereitet")
        return []

    df_buchungen = pd.DataFrame(df_buchungen)
    logger.debug(
        f"get_kursempfehlungen: DataFrame erstellt mit {len(df_buchungen)} Einträgen"
    )

    # Schwierigkeit als ordinales Feature
    schwierigkeits_map = {"Einfach": 0, "Mittel": 1, "Schwer": 2}
    df_buchungen["schwierigkeit_num"] = df_buchungen["schwierigkeit"].map(
        schwierigkeits_map
    )

    # Trend pro Typ bestimmen (letzte 3 Buchungen)
    empfehlungen = []
    typen = df_buchungen["typ"].unique()
    logger.debug(f"get_kursempfehlungen: Verarbeite {len(typen)} Kurstypen: {typen}")

    for typ in typen:
        df_typ = df_buchungen[df_buchungen["typ"] == typ].sort_values("datum")
        logger.debug(f"get_kursempfehlungen: Typ '{typ}' hat {len(df_typ)} Buchungen")

        if len(df_typ) < 2:
            logger.debug(
                f"get_kursempfehlungen: Typ '{typ}' übersprungen (weniger als 2 Buchungen)"
            )
            continue

        # CatBoost für Trend (Regression auf Schwierigkeit)
        X = np.arange(len(df_typ)).reshape(-1, 1)
        y = df_typ["schwierigkeit_num"].values

        if len(set(y)) < 2:
            logger.debug(
                f"Typ '{typ}' übersprungen: Target hat nur einen Wert: {set(y)}"
            )
            continue

        model = CatBoostClassifier(
            iterations=10,
            depth=2,
            learning_rate=1,
            loss_function="MultiClass",
            verbose=0,
        )
        model.fit(X, y)

        # Vorhersage für nächste Buchung
        next_idx = np.array([[len(df_typ)]])
        pred = int(model.predict(next_idx)[0][0])
        logger.debug(
            f"get_kursempfehlungen: Typ '{typ}' - vorhergesagte Schwierigkeit: {pred}"
        )

        # Empfohlene Schwierigkeit
        schwierigkeits_empf = [k for k, v in schwierigkeits_map.items() if v == pred]
        if not schwierigkeits_empf:
            logger.warning(
                f"get_kursempfehlungen: Keine Schwierigkeit für Wert {pred} gefunden"
            )
            continue

        schwierigkeits_empf = schwierigkeits_empf[0]
        logger.debug(
            f"get_kursempfehlungen: Typ '{typ}' - empfohlene Schwierigkeit: {schwierigkeits_empf}"
        )

        # Passenden Kurs finden
        passende_kurse = [
            k
            for k in kurse
            if k.typ == typ and k.schwierigkeitsgrad == schwierigkeits_empf
        ]
        if not passende_kurse:
            logger.warning(
                f"get_kursempfehlungen: Keine Kurse gefunden für Typ '{typ}' mit Schwierigkeit '{schwierigkeits_empf}'"
            )
            continue

        kurs_empf = passende_kurse[0]
        logger.debug(
            f"get_kursempfehlungen: Empfohlener Kurs: {kurs_empf.name} (ID: {kurs_empf.id})"
        )

        # Nächster Termin ab heute
        heute = datetime.now().date()
        termine_kurs = [t for t in termine if t.kurs.id == kurs_empf.id]
        logger.debug(
            f"get_kursempfehlungen: {len(termine_kurs)} Termine für Kurs {kurs_empf.id} gefunden"
        )

        termine_kurs = sorted(termine_kurs, key=lambda t: t.datum)
        naechster_termin = None

        for t in termine_kurs:
            try:
                termin_datum = t.datum
                if isinstance(termin_datum, str):
                    termin_datum = datetime.strptime(termin_datum, "%Y-%m-%d").date()
                if termin_datum >= heute:
                    naechster_termin = t
                    logger.debug(
                        f"get_kursempfehlungen: Nächster Termin gefunden: {termin_datum}"
                    )
                    break
            except Exception as e:
                logger.warning(
                    f"get_kursempfehlungen: Fehler beim Verarbeiten von Termin: {e}"
                )
                continue

        if naechster_termin:
            empfehlungen.append(
                {
                    "typ": typ,
                    "kurs": kurs_empf,
                    "termin": naechster_termin,
                    "datum": naechster_termin.datum,
                    "uhrzeit": naechster_termin.uhrzeit,
                }
            )
            logger.info(
                f"get_kursempfehlungen: Empfehlung erstellt für Typ '{typ}', Kurs '{kurs_empf.name}', Termin {naechster_termin.datum}"
            )
        else:
            logger.warning(
                f"get_kursempfehlungen: Kein zukünftiger Termin für empfohlenen Kurs '{kurs_empf.name}' gefunden"
            )

    logger.info(
        f"get_kursempfehlungen: Insgesamt {len(empfehlungen)} Empfehlungen erstellt"
    )
    return empfehlungen


def show_kursbuchungen():
    """Zeigt die Kursbuchungsseite mit Kalender und Empfehlungen an."""
    
    st.subheader("Kurs-Termine buchen")
    user_id = str(st.session_state.mitgliedsnummer)
    
    # Empfehlungen anzeigen
    empfehlungen = get_kursempfehlungen()
    if empfehlungen:
        st.markdown("### Persönliche Kurs-Empfehlungen")
        for emp in empfehlungen:
            kurs = emp["kurs"]
            termin = emp["termin"]
            st.markdown(
                f"**{kurs.name}** ({kurs.typ}, Schwierigkeit: {kurs.schwierigkeitsgrad})<br>Nächster Termin: {emp['datum']} um {emp['uhrzeit']}",
                unsafe_allow_html=True,
            )

            schon_gebucht = user_id in getattr(termin, "kursbuchungen", [])
            max_teilnehmer = getattr(termin.kurs, "max_teilnehmer", 0)
            anzahl_buchungen = len(getattr(termin, "kursbuchungen", []))
            if schon_gebucht:
                st.info("Sie haben diesen Termin bereits gebucht.")
            elif int(anzahl_buchungen) >= int(max_teilnehmer):
                st.warning("Kurs ist voll!")
            else:
                if st.button(
                    f"Empfohlenen Termin buchen: {kurs['name']} {emp['datum']} {emp['uhrzeit']}"
                ):
                    try:
                        kurstermin.teilnehmer_hinzufuegen(user_id)
                        kurstermin_repo = get_kurstermineRepo(kurs.id)
                        kurstermin_repo.update(
                            predicate=lambda u: u.id == kurstermin.id,
                            updater=lambda u: setattr(
                                u,
                                "kursbuchungen",
                                getattr(u, "kursbuchungen", []) + [user_id],
                            ),
                        )
                        st.success("Empfohlener Termin erfolgreich gebucht!")
                        logger.info(
                            f"Empfohlene Buchung erfolgreich: Mitglied {user_id}, Kurs {kurs['id']}, Termin {termin.id}"
                        )
                    except Exception as e:
                        logger.error(
                            f"Fehler beim Buchen des empfohlenen Termins: {e}",
                            exc_info=True,
                        )
                        st.error(f"Fehler beim Buchen: {str(e)}")
    else:
        st.info(
            "Keine persönlichen Empfehlungen verfügbar. Buchen Sie gerne einen Kurs aus dem Kalender unten!"
        )

    # Kalender anzeigen
    try:
        termine = get_all_kurstermine()
        logger.debug(f"{len(termine)} Kurstermine für Kalender geladen.")

    except Exception as e:
        logger.error(f"Fehler beim Laden der Kurstermine: {e}", exc_info=True)
        st.error("Fehler beim Laden der Kurstermine.")
        return

    events = [
        {
            "id": t.id,
            "title": t.kurs.name,
            "start": f"{t.datum}T{t.uhrzeit}:00",
            "end": f"{t.datum}T{t.uhrzeit}:00",
            "color": (
                "green" if user_id in t.kursbuchungen else "blue"
            ), 
        }
        for t in termine
    ]

    try:
        selected = calendar(
            events=events,
            options={"selectable": True, "height": 500, "locale": "de"},
            custom_css=".fc-event {cursor:pointer;}",
        )
        st.info(
            "Klicken Sie auf einen Termin im Kalender, um hier mehr Informationen anzuzeigen."
        )
        logger.debug("Kalender erfolgreich angezeigt.")
    except Exception as e:
        logger.error(f"Fehler beim Anzeigen des Kalenders: {e}", exc_info=True)
        st.error("Fehler beim Anzeigen des Kalenders.")
        return

    # Verarbeitung der Kalender-Event-Auswahl    
    if selected and selected.get("callback") == "eventClick":
        logger.info(f"Kalender-Event ausgewählt: {selected['eventClick']['event']}")
        st.session_state.selected_event = selected["eventClick"]["event"]
    else:
        logger.debug(
            "Kein Kalender-Event ausgewählt oder Event-Daten fehlen. selected: %s",
            selected,
        )

    event = st.session_state.get("selected_event", None)
    if event:
        logger.debug(f"Ausgewähltes Event: {event}")
        try:
            sel = next(
                (t for t in termine if str(t.id) == str(event["id"])),
                None,
            )
        except Exception as e:
            logger.error(
                f"Fehler bei der Suche nach passendem Termin: {e}", exc_info=True
            )
            st.error("Fehler bei der Verarbeitung des ausgewählten Termins.")
            return

        if sel:
            kurs = sel.kurs
            logger.info(f"Passenden Kurs gefunden: {kurs.name} (ID: {kurs.id})")
            kurstermin = sel
            logger.info(
                f"Passenden Kurstermin gefunden: {kurstermin.uhrzeit} (ID: {kurstermin.id})"
            )
            try:
                st.markdown(f"""
					### 🧭 **{kurs.name}**
					**Datum:** {kurstermin.datum}  
					**Uhrzeit:** {kurstermin.uhrzeit}  
					**Beschreibung:** {kurs.beschreibung}  
					**Dauer:** {kurs.dauer} Minuten 
					**Schwierigkeitsgrad:** {kurs.schwierigkeitsgrad}
					""")
            except Exception as e:
                logger.error(
                    f"Fehler beim Anzeigen der Kursdetails: {e}", exc_info=True
                )
                st.error("Fehler beim Anzeigen der Kursdetails.")
                return

            try:
                schon_gebucht = user_id in getattr(kurstermin, "kursbuchungen", [])
                logger.info(
                    f"Mitglied {user_id} Buchungsstatus für Termin {getattr(kurstermin, 'id', 'unbekannt')}: {'bereits gebucht' if schon_gebucht else 'noch nicht gebucht'}"
                )
            except Exception as e:
                logger.error(
                    f"Fehler beim Prüfen des Buchungsstatus: {e}", exc_info=True
                )
                st.error("Fehler beim Prüfen des Buchungsstatus.")
                return

            if schon_gebucht:
                st.info("Sie haben diesen Termin bereits gebucht.")
            else:
                try:
                    max_teilnehmer = getattr(kurs, "max_teilnehmer", 0)
                    anzahl_buchungen = len(getattr(kurstermin, "kursbuchungen", []))
                    logger.info(
                        f"Teilnehmerzahl für Kurs {kurs.id}: {anzahl_buchungen}/{max_teilnehmer}"
                    )
                except Exception as e:
                    logger.error(
                        f"Fehler beim Ermitteln der Teilnehmerzahl: {e}",
                        exc_info=True,
                    )
                    st.error("Fehler beim Ermitteln der Teilnehmerzahl.")
                    return

                try:
                    if int(anzahl_buchungen) < int(max_teilnehmer):
                        logger.info(
                            f"Mitglied {user_id} versucht, Termin {getattr(kurstermin, 'id', 'unbekannt')} zu buchen. Aktuelle Teilnehmerzahl: {anzahl_buchungen}/{max_teilnehmer}"
                        )
                        if st.button("Diesen Termin buchen"):
                            try:
                                kurstermin.teilnehmer_hinzufuegen(user_id)
                                kurstermin_repo = get_kurstermineRepo(kurs.id)
                                kurstermin_repo.update(
                                    predicate=lambda u: u.id == kurstermin.id,
                                    updater=lambda u: setattr(
                                        u,
                                        "kursbuchungen",
                                        getattr(u, "kursbuchungen", []) + [user_id],
                                    ),
                                )

                                st.success("Erfolgreich gebucht!")
                                logger.info(
                                    f"Buchung erfolgreich: Mitglied {user_id}, Kurs {kurs.id}, Termin {kurstermin.id}"
                                )
                                st.session_state.selected_event = None
                            except Exception as e:
                                logger.error(f"Fehler beim Buchen: {e}", exc_info=True)
                                st.error(f"Fehler beim Buchen: {str(e)}")
                    else:
                        st.warning("Kurs ist voll!")
                        logger.warning(
                            f"Kurs {kurs.id} am Termin {kurstermin.id} ist voll."
                        )
                except Exception as e:
                    logger.error(
                        f"Fehler beim Vergleich Teilnehmerzahl/max_teilnehmer: {e}",
                        exc_info=True,
                    )

        else:
            logger.info(f"Kein passender Kurs gefunden für Event: {event}")
    else:
        logger.debug("Kein Event in session_state.selected_event gefunden.")
