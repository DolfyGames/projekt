import customtkinter
from data import add_buchung
from gui import set_update_buchungen
class Popup():
    def create_pop_up(self):
        add_buchung = customtkinter.CTkToplevel()
        add_buchung.geometry("500x400")
        label = customtkinter.CTkLabel(add_buchung, text="Buchung hinzufügen")
        label.grid(row=0,column=0)

        label_title = customtkinter.CTkLabel(add_buchung, text="Titel")
        label_title.grid(row=1, column=0)
        title = customtkinter.CTkEntry(add_buchung,placeholder_text="Titel")
        title.grid(row=1, column=1)

        label_wert = customtkinter.CTkLabel(add_buchung, text="Wert")
        label_wert.grid(row=2, column=0)
        wert = customtkinter.CTkEntry(add_buchung,placeholder_text="Wert")
        wert.grid(row=2, column=1)