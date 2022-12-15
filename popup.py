import customtkinter
from data import add_buchung, add_konto, get_konten
class Popup():
    def create_pop_up_buchung(self):
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

        def set_selected(choice):
            if choice == "Weiteres Konto hinzufügen":
                #selected_konto = add_konto()
                print("bruh")
        konten = get_konten()
        select_konto = customtkinter.StringVar(value="Wählen sie ein Konto")
        values_ = ["Wählen sie ein Konto",konten,"Weiteres Konto hinzufügen"]
        select_konto = customtkinter.CTkOptionMenu(master = add_buchung, text="Konto",values=values_,command=set_selected,variable=select_konto)
        select_konto.grid(row=3, column=1)


