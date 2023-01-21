import customtkinter
import datetime
# erstellt ein Popup-Fenster, um eine Buchunghinzuzufügen
# Quelle:
        # https://github.com/TomSchimansky/CustomTkinter (dokumentation zu customtkiner)
        # https://docs.python.org/3/library/tk.html (dokumentation tkinter)

class Popup_Buchung():
    def __init__(self, datamanager,buchung=None):
        self.datamanager = datamanager
        self.buchung = buchung
    def create_pop_up_buchung(self):
        add_buchung_fenster = customtkinter.CTkToplevel()
        add_buchung_fenster.geometry("700x500")
        label = customtkinter.CTkLabel(add_buchung_fenster, text="Buchung hinzufügen")
        label.grid(row=0, column=1)
######## row 1
        label_title = customtkinter.CTkLabel(add_buchung_fenster, text="Titel")
        label_title.grid(row=1, column=0)
        title = customtkinter.CTkEntry(add_buchung_fenster, placeholder_text="Titel")
        title.grid(row=1, column=1)
######## row 2
        label_wert = customtkinter.CTkLabel(add_buchung_fenster, text="Wert")
        label_wert.grid(row=2, column=0)
        values = ["Einzahlung (+)", "Zahlungsart", "Auszahlung (-)"]
        def check_input_in_out(choice):
            if choice != "Zahlungsart":
                select_in_out.configure(text_color="white")
                
        select_in_out = customtkinter.CTkOptionMenu(master=add_buchung_fenster, values=values, command=check_input_in_out)
        select_in_out.grid(row=2, column=1)
        select_in_out.set("Zahlungsart")
       
        # sorgt dafür, dass nur floats eingetragen werden können
        def check_input(old, new,status,position, place_holder_text):
            if new == place_holder_text: # erlaubt den Platzhalter im eingabefeld 
                return True
            elif new == ".": # erlaubt es Punkte einzugeben (da man sonst keine floats eingeben könnte (1. != float -> wäre ohne dies nicht möglich))
                if status == "1": # ermöglicht das löschen des punktes (1 = eingabe; 0 = löschung) -> überprüft nur die Anzahl der Punkte bei einer Eingabe
                    if (old+new).count(".") > 1:  # überprüft die Anzahl der Punkte im String und verhindert, dass mehr als 2 dort eingegeben werden
                        return False
                return True
            else:               # wenn alle oberen anforderungen erfüllt sind wird final geprüft, ob der eingegebene wert einem float entspricht
                try:             # Quelle: https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
                    float(old+new)
                    eingabe_string = old+new
                    if eingabe_string.count(".")!=0:
                        if (int(position) - eingabe_string.index(".")) <= 2: # limitiert die eingabe auf 2 nachkommastellen    # Quelle https://www.programiz.com/python-programming/methods/string/index
                            wert.configure(text_color="white")
                            return True
                        else:
                            wert.configure(text_color="red")
                            return False
                    else: 
                        return True
                except ValueError:
                    wert.configure(text_color="red")
                    return False
        # Quelle: https://www.geeksforgeeks.org/python-tkinter-validating-entry-widget/
        check_input = add_buchung_fenster.register(check_input)
        wert = customtkinter.CTkEntry(add_buchung_fenster, placeholder_text="Wert",validate="key", validatecommand=(check_input, "%s", "%S", "%d","%i","Wert"))
        wert.grid(row=2, column=2)
        label_währung = customtkinter.CTkLabel(add_buchung_fenster, text="Euro")
        label_währung.grid(row=2, column=3)
######## row 3
        label_konto = customtkinter.CTkLabel(add_buchung_fenster, text="Konto")
        label_konto.grid(row=3, column=0)
        def set_selected(choice):
            if choice == "Weiteres Konto hinzufügen":
                konto_popup = Popup_Konto()
                konto_popup.create_pop_up_konto(values=values_, parent_optionmenu=select_konto, datamanager = self.datamanager)

            if choice != "Wählen sie ein Konto" and choice != "Weiteres Konto hinzufügen":
                select_konto.configure(text_color="white")
        konten = list(map(lambda x: x["name"],self.datamanager.get_konten()))
        select_konto = customtkinter.StringVar(value="Wählen sie ein Konto")
        values_ = ["Wählen sie ein Konto"]
        values_.extend(konten)
        values_.append("Weiteres Konto hinzufügen")
        select_konto = customtkinter.CTkOptionMenu(master=add_buchung_fenster, values=values_, command=set_selected)
        select_konto.grid(row=3, column=1)
        select_konto.set("Wählen sie ein Konto")
######## row 4 
        label_kategorien = customtkinter.CTkLabel(add_buchung_fenster, text="Kategorie")
        label_kategorien.grid(row=4, column=0)
        selected = []
        def create_kat_selection(): # <- erstell die kategorie auswahl (in eine Funktion gepackt, damit man es aktualisieren kann)
            self.kategorien_ = list(self.datamanager.get_kategorien())
            self.kategorien_.sort()
            self.kategorien_.insert(0,"Hinzufügen")

            self.kat_btn_dict = {}
            j=0
            for i in self.kategorien_:
                j+=1
                def clicked_kategorie(name=i, id=j):
                    if name == "Hinzufügen":
                        neue_kategorie = customtkinter.CTkInputDialog(title="Kategorie hinzufügen", text="Benennen sie die neue Kategorie")
                        input_ = neue_kategorie.get_input()
                        if input_ != "":
                            self.datamanager.add_kategorie(input_)
                            create_kat_selection()
                    elif self.kat_btn_dict[id].cget("fg_color")=="transparent":    
                        selected.append(name)
                        self.kat_btn_dict[id].configure(fg_color="blue")
                    else:
                        selected.remove(name)
                        self.kat_btn_dict[id].configure(fg_color="transparent")
                    
                self.kat_btn_dict[j] = customtkinter.CTkButton(master=add_buchung_fenster, text=i, fg_color="transparent", font=("TkDefaultFont", 12), width=50, height=14, command=clicked_kategorie, border_color="white", border_width=1)
                self.kat_btn_dict[j].grid(row = 4, column=j)  
        create_kat_selection()  

######## row 5 
        label_datum = customtkinter.CTkLabel(add_buchung_fenster, text="Datum")
        label_datum.grid(row=5, column=0)
        datum = customtkinter.CTkEntry(add_buchung_fenster, placeholder_text="DD.MM.YYYY")
        datum.grid(row=5, column=1)
######## row 6 
        def finish_buchung():
            title_ = title.get()
            in_out = select_in_out.get()
            wert_ = wert.get()
            konto_ = select_konto.get()

            # checked ob überall etwas eingetragen wurde und ob die Eingaben verwendet werden können
            def check():
                check_ = True
                if title_ == "":
                    title.configure(placeholder_text_color="red")
                    check_ = False

                if in_out == "Zahlungsart":
                    select_in_out.configure(text_color="red")
                    check_ = False

                if wert_ == "":
                    wert.configure(placeholder_text_color="red")
                    check_ = False

                if konto_ == "Wählen sie ein Konto" or konto_ == "Weiteres Konto hinzufügen":
                    select_konto.configure(text_color="red")
                    check_ = False
                
                try: # Überprüft, ob das datum im passenden Format ist 
                    datetime.datetime.strptime(datum.get(), "%d.%m.%Y") #Quelle: https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
                except ValueError:
                    datum.configure(text_color="red")
                    check_ = False
                    
                return check_

            if check() == True:
                if self.buchung == None:
                    self.datamanager.add_buchung(
                                title=title.get(), 
                                wert=float(wert.get()),
                                buchungs_art="in" if in_out.__contains__("+") else "out", # da die String in der Auswahl (aus Verständnissgründen) nicht der verarbeitbaren Strings entsprechen, werden sie hier umgewandelt
                                konto=konto_,
                                kategorie=selected,
                                zeitpunkt=datum.get()
                                )
                    add_buchung_fenster.destroy()
                else:
                    neu ={
                                "title":title.get(), 
                                "wert":float(wert.get()),
                                "buchungs_art":"in" if in_out.__contains__("+") else "out", # da die String in der Auswahl (aus Verständnissgründen) nicht der verarbeitbaren Strings entsprechen, werden sie hier umgewandelt
                                "konto":konto_,
                                "kategorie":selected,
                                "zeitpunkt":datum.get()
                    }
                    self.datamanager.edit_remove_buchung(self.buchung,neu)
                    add_buchung_fenster.destroy()


        fertig_btn = customtkinter.CTkButton(add_buchung_fenster,text="Fertig", command=finish_buchung)
        fertig_btn.grid(row=6, sticky="s", column=1)

        if self.buchung != None:
            title.insert(0,self.buchung["title"])
            select_in_out.set("Auszahlung (-)" if self.buchung["buchungs_art"] == "out" else "Einzahlung (+)") # in-line if else
            wert.insert(0,str(f'{self.buchung["wert"]:.2f}'))
            select_konto.set(self.buchung["konto"])
            for kats in self.buchung["kategorie"]:
                self.kat_btn_dict[self.kategorien_.index(kats)+1].configure(fg_color="blue")
                selected.append(kats)
            datum.insert(0,self.buchung["zeitpunkt"])
            
            def löschen():
                self.datamanager.edit_remove_buchung(self.buchung)
                add_buchung_fenster.destroy()
                
            löschen_btn = customtkinter.CTkButton(add_buchung_fenster,text="Löschen", command=löschen, fg_color="red")
            löschen_btn.grid(row=6, sticky="s", column=2)

####################################################################################
# erstellt ein Popup-Fenster, um ein Konto hinzuzufügen


class Popup_Konto():
    def create_pop_up_konto(self, values, parent_optionmenu, datamanager):
        # instanziierte das Popup-Fenster und setzt die größe Fest
        add_konto_fenster = customtkinter.CTkToplevel()
        add_konto_fenster.geometry("500x200")

        # Oberfläche, um Name und Kontonummer eingeben zu können
        label = customtkinter.CTkLabel(add_konto_fenster, text="Konto hinzufügen")
        label.grid(row=0, column=0)

        label_name = customtkinter.CTkLabel(add_konto_fenster, text="Name")
        label_name.grid(row=1, column=0)
        name = customtkinter.CTkEntry(add_konto_fenster, placeholder_text="Name")
        name.grid(row=1, column=1)

        label_kontonummer = customtkinter.CTkLabel(add_konto_fenster, text="Kontonummer")
        label_kontonummer.grid(row=2, column=0)
        kontonummer = customtkinter.CTkEntry(add_konto_fenster, placeholder_text="Kontonummer")
        kontonummer.grid(row=2, column=1)

        # Funktion, um das neue Konto hinzufügen
        def complete_add_konto():
            datamanager.add_konto(name.get(), kontonummer.get())# <--- Fügt ein neues Konto des Konto-Dict zu, mit den Daten der Eingabefelder
            values.insert(len(values)-1, name.get())# <--- Akutalisiert die Kontoliste für das OptionMenus
            parent_optionmenu.configure(values=values)# <--- Aktualisiert das OptionMenu
            parent_optionmenu.set(name.get())
            add_konto_fenster.destroy()                 # <--- Schließt das Popup-Fenster

        complete_button = customtkinter.CTkButton(master=add_konto_fenster, text="Konto hinzufügen", command=complete_add_konto)
        complete_button.grid(row=3)
