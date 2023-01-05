import json
import os 
import datetime

class Data():
    def __init__(self):
        self.konten = []
        self.kategorien = []
        self.buchungen = []
        
        self.sort_state = False
        self.last_sort_paramter = ""
        self.last_sort_reverse = False
        
        self.filter_state = False
        self.last_filter_parameter = []

    def set_gui(self,gui_):
        self.gui = gui_

    def load(self):
        if os.path.exists("data.json"):
            # Öffne die Datei zum Lesen
            with open("data.json", "r") as file:
                # Laden der Daten aus der Datei
                alles = json.load(file)
                self.konten = alles["konten"]
                self.kategorien = alles["kategorien"]
                self.buchungen = alles ["buchungen"]
                self.anzeige_liste = self.buchungen.copy()
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
        
        self.anzeige_liste = list(self.buchungen)
        if self.sort_state == True:
            self.sort(self.last_sort_paramter,self.last_sort_reverse)
        if self.filter_state == True:
            self.filtern(state=True)
        
        self.gui.set_update_buchungen()
        self.gui.set_update_kontostand()
                
    def add_konto(self,name, kontonummer):
        self.konten.append({"name": name, "kontonummer": kontonummer})
        self.gui.set_update_filter()


    def add_kategorie(self,name):
        self.kategorien.append(name)

        
    # ermöglich daten zu ändern oder zu entfernen
    # changes ist entweder remove oder die komplette buchung mit den änderungen
    def edit_remove_buchung(self,buchung, neu=None):
        if neu == None:
            self.buchungen.remove(buchung)
        else:
            self.buchungen[self.buchungen.index(buchung)] = neu
            
        self.anzeige_liste = list(self.buchungen)
        if self.sort_state == True:
            self.sort(self.last_sort_paramter,self.last_sort_reverse)
        if self.filter_state == True:
            self.filtern(state=True)
        
        self.gui.set_update_buchungen()
        self.gui.set_update_kontostand()
    def filtern(self,state,key=None):
        if state:
            self.filter_state = True
            if key != None:
                self.last_filter_parameter.append(key)
        else:
            self.anzeige_liste = self.buchungen.copy()
            
            if self.last_filter_parameter.__contains__(key):
                self.last_filter_parameter.remove(key)
                
            if self.last_filter_parameter == []:
                self.filter_state = False
        
        if self.filter_state:

            def custom_filter(i):
                value_list = []                     # wandelt die values des dicts so um (in einen 1 dimensinalen array), sodass man schauen kann, ob ein bestimmter string dort drinnen ist 
                for obj in list(i.values()):
                    if isinstance(obj,list):
                        value_list.extend(obj)
                    else:
                        value_list.append(obj)
                        
                if all(filters in value_list for filters in self.last_filter_parameter):    # für filters in der Liste wird überprüft, ob sich dieser String irgendwo in den Werten vom dict wiederfindet   #Quelle: https://stackoverflow.com/questions/405516/if-all-in-list-something                    
                    return True
                else:
                    return False
                  
            self.anzeige_liste = list(filter(custom_filter,self.anzeige_liste))
        self.gui.set_update_buchungen()
            
    def sort(self,eigenschaft,_reverse):

        self.last_sort_paramter = eigenschaft
        self.last_sort_reverse = _reverse
        self.sort_state = True
        
        if eigenschaft == "wert":
            self.anzeige_liste = list(sorted(self.anzeige_liste,key=lambda x: x[eigenschaft],reverse=_reverse))
        elif eigenschaft == "zeitpunkt":
            def get_usefull_date(datum):
                date = datetime.datetime.strptime(datum, '%d.%m.%Y')
                return(date.year, date.month, date.day)
            
            self.anzeige_liste = list(sorted(self.anzeige_liste,key=lambda x: get_usefull_date(x[eigenschaft]),reverse=_reverse))
        else:
            self.sort_state = False
        self.gui.set_update_buchungen()
        
    # gibt die Buchungsliste, Kontenliste und Kategorienliste zurück
    def get_buchungen(self):
        if self.sort_state == False and self.filter_state == False:
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