buchungen = [{"title":"title","wert":"wert","buchungs_art":"in","zeitpunkt":"zeitpunkt"},{"title":"title","wert":"wert","buchungs_art":"out","zeitpunkt":"zeitpunkt"}]


# fügt eine Buchung hinzu
def add_buchung(title,wert,buchungs_art,zeitpunkt):
    buchungen.append({"title":title,"wert":wert,"buchungs_art":buchungs_art,"zeitpunkt":zeitpunkt})


# ermöglich daten zu ändern oder zu entfernen
# changes ist entweder remove oder die komplette buchung mit den änderungen
def edit_remove_buchung(buchung, changes):
    if changes == "remove":
        buchungen.remove(buchung)
    else:
        buchungen[buchungen.index(buchung)] = changes

# gibt die Buchungsliste zurück
def get_buchungen():
    return buchungen;