import json
konten = []
kategorien = ["Test1","Test2"]
buchungen = [{"title": "title",
              "wert": "wert",
              "buchungs_art": "in",
              "konto": "konto",
              "kategorie": [],
              "zeitpunkt":"zeitpunkt"},
             {"title": "title",
              "wert": "wert", "buchungs_art": "out",
                 "konto": "konto",
                 "kategorie": [],
                 "zeitpunkt":"zeitpunkt"}]

alles = {"konten": konten, "kategorien": kategorien, "buchungen": buchungen}


def load():
    # Öffne die Datei zum Lesen
    with open("data.json", "r") as file:
        # Laden der Daten aus der Datei
        alles = json.load(file)


def save():
    alles = {"konten": konten, "kategorien": kategorien, "buchungen": buchungen}
    # Öffne eine Datei zum Schreiben
    with open("data.json", "w") as file:
        # Schreibe die Daten im JSON-Format in die Datei
        json.dump(alles, file)

# fügt eine Buchung hinzu


def add_buchung(title, wert, buchungs_art, konto, kategorie, zeitpunkt):
    buchungen.append({
        "title": title,
        "wert": wert,
        "buchungs_art": buchungs_art,
        "konto": konto,
        "kategorie": kategorie,
        "zeitpunkt": zeitpunkt
    })
    print(buchungen)  # muss wieder weg


def add_konto(name, kontonummer):
    konten.append({"name": name, "kontonummer": kontonummer})


def add_kategorie(name):
    kategorien.append(name)
    print(kategorien) # muss wieder weg
    
# ermöglich daten zu ändern oder zu entfernen
# changes ist entweder remove oder die komplette buchung mit den änderungen
def edit_remove_buchung(buchung, changes):
    if changes == "remove":
        buchungen.remove(buchung)
    else:
        buchungen[buchungen.index(buchung)] = changes

# gibt die Buchungsliste, Kontenliste und Kategorienliste zurück


def get_buchungen():
    return buchungen


def get_konten():
    return konten


def get_kategorien():
    return kategorien
