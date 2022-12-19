import customtkinter
from data import add_buchung, add_konto, get_konten

# erstellt ein Popup-Fenster, um eine Buchunghinzuzufügen 
class Popup_Buchung():
    def create_pop_up_buchung(self):
        add_buchung_fenster = customtkinter.CTkToplevel()
        add_buchung_fenster.geometry("500x400")
        label = customtkinter.CTkLabel(add_buchung_fenster, text="Buchung hinzufügen")
        label.grid(row=0,column=0)

        label_title = customtkinter.CTkLabel(add_buchung_fenster, text="Titel")
        label_title.grid(row=1, column=0)
        title = customtkinter.CTkEntry(add_buchung_fenster,placeholder_text="Titel")
        title.grid(row=1, column=1)

        label_wert = customtkinter.CTkLabel(add_buchung_fenster, text="Wert")
        label_wert.grid(row=2, column=0)
        wert = customtkinter.CTkEntry(add_buchung_fenster,placeholder_text="Wert")
        wert.grid(row=2, column=1)
        
        def set_selected(choice):
            if choice == "Weiteres Konto hinzufügen":
                konto_popup = Popup_Konto()
                konto_popup.create_pop_up_konto(values=values_,optionmenu=select_konto)
        konten = get_konten()
        select_konto = customtkinter.StringVar(value="Wählen sie ein Konto")
        values_ = ["Wählen sie ein Konto"]
        values_.extend(konten)
        values_.append("Weiteres Konto hinzufügen")
        select_konto = customtkinter.CTkOptionMenu(master = add_buchung_fenster,values=values_,command=set_selected)
        select_konto.grid(row=3, column=1)
        select_konto.set("Wählen sie ein Konto")


def create_popup_buchung():
    this = Popup_Buchung()
    this.create_pop_up_buchung()
#############################################################################################################################
# erstellt ein Popup-Fenster, um ein Konto hinzuzufügen
class Popup_Konto():
    def create_pop_up_konto(self,values,parent_optionmenu):
        #instanziierte das Popup-Fenster und setzt die größe Fest
        add_konto_fenster = customtkinter.CTkToplevel()
        add_konto_fenster.geometry("500x200")

        # Oberfläche, um Name und Kontonummer eingeben zu können
        label = customtkinter.CTkLabel(add_konto_fenster, text="Konto hinzufügen")
        label.grid(row=0,column=0)

        label_name = customtkinter.CTkLabel(add_konto_fenster, text="Name")
        label_name.grid(row=1, column=0)
        name = customtkinter.CTkEntry(add_konto_fenster,placeholder_text="Name")
        name.grid(row=1, column=1)

        label_kontonummer = customtkinter.CTkLabel(add_konto_fenster, text="Kontonummer")
        label_kontonummer.grid(row=2, column=0)
        kontonummer = customtkinter.CTkEntry(add_konto_fenster,placeholder_text="Kontonummer")
        kontonummer.grid(row=2, column=1)
        
        # Funktion, um das neue Konto hinzufügen 
        def complete_add_konto():
            add_konto(name.get(), kontonummer.get())    # <--- Fügt ein neues Konto des Konto-Dict zu, mit den Daten der Eingabefelder
            values.insert(len(values)-1,name.get())     # <--- Akutalisiert die Kontoliste für das OptionMenus
            parent_optionmenu.configure(values=values)  # <--- Aktualisiert das OptionMenu

            add_konto_fenster.destroy()                 # <--- Schließt das Popup-Fenster

        complete_button = customtkinter.CTkButton(master= add_konto_fenster,text="Konto hinzufügen", command=complete_add_konto)
        complete_button.grid(row=3)