import json
import os 
import datetime

class Data():
    def __init__(self):
        self.konten = []
        self.kategorien = ["Test1","Test2"]
        self.buchungen = [{"title": "title",
                    "wert": 11.00,
                    "buchungs_art": "in",
                    "konto": "konto",
                    "kategorie": ["Test1"],
                    "zeitpunkt":"01.02.2012"},
                    {"title": "title",
                    "wert": 12.00, 
                    "buchungs_art": "out",
                        "konto": "konto",
                        "kategorie": ["Test2"],
                        "zeitpunkt":"02.02.2012"}]

        self.anzeige_liste = self.buchungen.copy()
        self.sort_state = False
        self.last_sort_paramter = ""
        self.last_sort_reverse = False




    def load(self):
        if os.path.exists("data.json"):
            # Öffne die Datei zum Lesen
            with open("data.json", "r") as file:
                # Laden der Daten aus der Datei
                alles = json.load(file)
                self.konten = alles["konten"]
                self.kategorien = alles["kategorien"]
                self.buchungen = alles ["buchungen"]
        else:
            self.save()


    def save(self):
        alles = {"konten": self.konten, "kategorien": self.kategorien, "buchungen": self.buchungen}
        # Öffne eine Datei zum Schreiben
        with open("data.json", "w") as file:
            # Schreibe die Daten im JSON-Format in die Datei
            json.dump(alles, file)

    # fügt eine Buchung hinzu


    def add_buchung(self,title, wert, buchungs_art, konto, kategorie, zeitpunkt):
        self.buchungen.append({
            "title": title,
            "wert": wert,
            "buchungs_art": buchungs_art,
            "konto": konto,
            "kategorie": kategorie,
            "zeitpunkt": zeitpunkt
        })

        if self.sort_state == True:
            self.sort(self.last_sort_paramter,self.last_sort_reverse)


    def add_konto(self,name, kontonummer):
        self.konten.append({"name": name, "kontonummer": kontonummer})


    def add_kategorie(self,name):
        self.kategorien.append(name)
        print(self.kategorien) # muss wieder weg
        
    # ermöglich daten zu ändern oder zu entfernen
    # changes ist entweder remove oder die komplette buchung mit den änderungen
    def edit_remove_buchung(self,buchung, changes):
        if changes == "remove":
            self.buchungen.remove(buchung)
        else:
            self.buchungen[self.buchungen.index(buchung)] = changes




    def sort(self,eigenschaft,_reverse):
        self.anzeige_liste.clear()
        self.last_sort_paramter = eigenschaft
        self.last_sort_reverse = _reverse
        self.sort_state = True
        
        if eigenschaft == "wert":
            self.anzeige_liste.extend(sorted(self.buchungen,key=lambda x: x[eigenschaft],reverse=_reverse))
        elif eigenschaft == "zeitpunkt":
            def get_usefull_date(datum):
                date = datetime.datetime.strptime(datum, '%d.%m.%Y')
                return(date.year, date.month, date.day)
            
            self.anzeige_liste.extend(sorted(self.buchungen,key=lambda x: get_usefull_date(x[eigenschaft]),reverse=_reverse))
        else:
            self.sort_state = False
        
    # gibt die Buchungsliste, Kontenliste und Kategorienliste zurück


    def get_buchungen(self):
        print(self.sort_state)
        if self.sort_state == False:
            return self.buchungen
        else:
            return self.anzeige_liste


    def get_konten(self):
        return self.konten


    def get_kategorien(self):
        return self.kategorien


    def get_kontostand(self):
        return self.calc_kontostand()

    def calc_kontostand(self):
        kontostand=0
        for buchung in self.buchungen:
            if buchung["buchungs_art"] == "in":
                kontostand += buchung["wert"]
            else:
                kontostand -= buchung["wert"]
                
        return kontostand
        
        
        