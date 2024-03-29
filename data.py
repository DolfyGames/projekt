import json
import os 
import datetime
import re

class Data():
    def __init__(self):
        self.konten = []
        self.kategorien = []
        self.buchungen = []
        
        self.sort_state = False
        self.last_sort_paramter = ""
        self.last_sort_reverse = False
        
        self.filter_state = False
        self.last_filter_paramter = {
            "filter": [],
            "suche": None
        }
        #self.last_filter_parameter = []
        #self.vorheriger_suchwert = None

    def set_gui(self,gui_):
        self.gui = gui_

    def load(self):                                             # lad die gespeichert Datei, fals vorhanden, wenn nicht erstellt es einen neue
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

    def save(self):                                           # speichert die daten in eine json datei
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
        if self.sort_state == True:                                         # fals die liste sortiert war wird sie hier wieder sortiert 
            self.sort(self.last_sort_paramter,self.last_sort_reverse)
        if self.filter_state == True:                                       # fals ein filter aktiv ist wird die liste neu gefilter
            self.filtern(state=True)
        
        self.gui.set_update_buchungen()                                     # aktualisiert die buchungsanzeige
        self.gui.set_update_kontostand()                                    # aktualisiert die Kontostandsanzeige
                
    def add_konto(self,name, kontonummer):                                  # fügt ein Konto den Daten hinzu 
        self.konten.append({"name": name, "kontonummer": kontonummer})
        self.gui.set_update_filter()
        
    def remove_konto(self,konto):                                           # entfernt ein Konto aus den Daten 
        self.konten.remove(konto)
        self.gui.set_update_filter()            # aktualisiert die Filteransicht

    def add_kategorie(self,name):                                           # fügt eine Kategorien den Daten hinzu
        if not self.kategorien.__contains__(name):
            self.kategorien.append(name)
            self.gui.set_update_filter()        # aktualisiert die Filteransicht
    def remove_kategorie(self,kategorie):                                   # entfernt eine Kategorie aus den Daten
        self.kategorien.remove(kategorie)
        self.gui.set_update_filter()            # aktualisiert die Filteransicht

        
    # ermöglich daten zu ändern oder zu entfernen
    # löscht oder ersetz die alte buchung 
    def edit_remove_buchung(self,buchung, neu=None):
        if neu == None:
            self.buchungen.remove(buchung)
        else:
            self.buchungen[self.buchungen.index(buchung)] = neu
            
        self.anzeige_liste = list(self.buchungen)
        if self.sort_state == True:
            self.sort(self.last_sort_paramter,self.last_sort_reverse)
        if self.filter_state == True:
            self.filtern_(art="update", add=False)
        
        self.gui.set_update_buchungen()                     # aktualisiert die buchungsanzeige
        self.gui.set_update_kontostand()                    # aktualisiert die Kontostandsanzeige
        self.gui.set_update_filter()                        # aktualisiert die Filteranzeige
    
    def filtern_(self,art,add,key=None):                    # ermöglicht es die Buchungen zu filtern 
        self.filter_state = True
        self.anzeige_liste = self.buchungen.copy()
        if art == "filtern":                                # überprüft, ob nach filter parametern oder nach dem suchparameter gefiltert werden soll und ändert dem entsprechend die werte im last_filter_parameter dict
            if add == True:
                self.last_filter_paramter["filter"].append(key)
            else:
                if self.last_filter_paramter["filter"].__contains__(key):
                    self.last_filter_paramter["filter"].remove(key)
                    
        elif art == "suche":
            self.last_filter_paramter["suche"] = key
            
        if self.last_filter_paramter["filter"] == [] and self.last_filter_paramter["suche"] == None:            # past nur den filter_state an 
            self.filter_state = False
        if self.filter_state:                   # der eigentliche filter
            def custom_filter(i):
                value_list = []     # wandelt die values des dicts so um (in einen 1 dimensinalen array), sodass man schauen kann, ob ein bestimmter string dort drinnen ist
                bool_list = []
                such_bool_list = []
                for obj in list(i.values()):        # zerlegt alle werte einer buchung in eine eindimensionale liste an strings
                    if isinstance(obj,list):
                        value_list.extend(obj)
                    else:
                        value_list.append(obj)
                if self.last_filter_paramter["suche"] != None:   # sollte ein Suchwert vorliegen wird geschaut, ob der gesuchte string irgendwo in der value_liste vorkommt
                    for values in value_list:
                        if re.search(str(self.last_filter_paramter["suche"]),str(values)):
                            such_bool_list.append(True)
                        else:
                            such_bool_list.append(False)
                    if True in such_bool_list:       
                        bool_list.append(True)
                    else:
                        bool_list.append(False)
                if self.last_filter_paramter["filter"] != []:                       # sollte ein filter wert vorliegen wird geschaut ob der filter wert als kategorie oder kontoname in der buchung vorliegt  
                    for filters in self.last_filter_paramter["filter"]:
                        if filters in i["kategorie"] or filters == i["konto"]:
                            bool_list.append(True)
                        else:
                            bool_list.append(False)
                        
                if all(bool_list):    # sollten alle werte dieser Liste True sein, so wird die Buchung nicht rausgefiltert   #Quelle: https://stackoverflow.com/questions/405516/if-all-in-list-something
                    return True
                else:
                    return False
                  
            self.anzeige_liste = list(filter(custom_filter,self.anzeige_liste))    # filtert die liste 

        if self.sort_state:                                                 # überprüft, ob die liste sortiert war und stößt den sortier vorgang erneut an sollte die liste sortiert gewesen sein 
            self.sort(self.last_sort_paramter,self.last_sort_reverse)  
        else:
            self.gui.set_update_buchungen() 
         
    def sort(self,eigenschaft,_reverse):            # sortiert die angezeigten buchungen 

        self.last_sort_paramter = eigenschaft
        self.last_sort_reverse = _reverse
        self.sort_state = True

        if eigenschaft == "wert":                                                                                   # sortiert entweder nach wert oder zeitpunkt (neu-alt)
            self.anzeige_liste = list(sorted(self.anzeige_liste,key=lambda x: x[eigenschaft],reverse=_reverse))
        elif eigenschaft == "zeitpunkt":
            def get_usefull_date(datum):                                    # wandelt das angezeigte datum in ein für das programm verwendbare datum um 
                date = datetime.datetime.strptime(datum, '%d.%m.%Y')
                return(date.year, date.month, date.day)
            
            self.anzeige_liste = list(sorted(self.anzeige_liste,key=lambda x: get_usefull_date(x[eigenschaft]),reverse=_reverse))
        else:
            self.sort_state = False
        self.gui.set_update_buchungen()         # aktualisiert die buchungsanzeige
        
    # gibt die Buchungsliste, Kontenliste, Kategorienliste und den Kontostand zurück
    def get_buchungen(self):
        if self.sort_state == False and self.filter_state == False:
            return self.buchungen
        else:
            return self.anzeige_liste

    def get_konten(self):
        return self.konten

    def get_kategorien(self):
        return self.kategorien

    def get_kontostand(self, konto="gesamt"):
        return self.calc_kontostand(konto)

    #berechnet den kontostand gesamt und jedes einzelnen kontos
    def calc_kontostand(self, konto):
        kontostand = 0
        if konto == "gesamt":
            for buchung in self.buchungen:
                if buchung["buchungs_art"] == "in":
                    kontostand += buchung["wert"]
                else:
                    kontostand -= buchung["wert"]
        else:
            for buchung in self.buchungen:
                if buchung["konto"] == konto:
                    if buchung["buchungs_art"] == "in":
                        kontostand += buchung["wert"]
                    else:
                        kontostand -= buchung["wert"]

        return kontostand
    
    # zählt wie oft ein konto oder eine katogerie verwendet wird und gibt diesen wert zurück 
    def get_verwendungszahl(self,konto_or_kategorie,name):
        verwendungszahl = 0
        if konto_or_kategorie == "konto":
            for buchung in self.buchungen:
                if buchung["konto"] == name:
                    verwendungszahl += 1
        else:
            for buchung in self.buchungen:
                if buchung["kategorie"].__contains__(name):
                    verwendungszahl += 1
        return verwendungszahl
        