import customtkinter
from data import add_buchung, add_konto, get_konten

# erstellt ein Popup-Fenster, um eine Buchunghinzuzufügen


class Popup_Buchung():
    def create_pop_up_buchung(self):
        add_buchung_fenster = customtkinter.CTkToplevel()
        add_buchung_fenster.geometry("500x400")
        label = customtkinter.CTkLabel(add_buchung_fenster, text="Buchung hinzufügen")
        label.grid(row=0, column=1)
########
        label_title = customtkinter.CTkLabel(add_buchung_fenster, text="Titel")
        label_title.grid(row=1, column=0)
        title = customtkinter.CTkEntry(add_buchung_fenster, placeholder_text="Titel")
        title.grid(row=1, column=1)
########
        label_wert = customtkinter.CTkLabel(add_buchung_fenster, text="Wert")
        label_wert.grid(row=2, column=0)
        values = ["Einzahlung (+)", "Zahlungsart", "Auszahlung (-)"]
        select_in_out = customtkinter.CTkOptionMenu(master=add_buchung_fenster, values=values)
        select_in_out.grid(row=2, column=1)
        select_in_out.set("Zahlungsart")
########        
        # sorgt dafür, dass nur floats eingetragen werden können
        def check_input(old, new,status, place_holder_text):
            # Quelle: https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
            if new == place_holder_text:
                return True
            elif new == ".": # überprüft die Anzahl der Punkte im String 
                if status == "1":
                    if (old+new).count(".") > 1:
                        return False
                return True
            else:
                try:
                    float(old+new)
                    wert.configure(text_color="white")
                    return True
                except ValueError:
                    wert.configure(text_color="red")
                    return False
        # Quelle: https://www.geeksforgeeks.org/python-tkinter-validating-entry-widget/
        check_input = add_buchung_fenster.register(check_input)
        wert = customtkinter.CTkEntry(add_buchung_fenster, placeholder_text="Wert",validate="key", validatecommand=(check_input, "%s", "%S", "%d","Wert"))
        wert.grid(row=2, column=2)
########
        label_konto = customtkinter.CTkLabel(add_buchung_fenster, text="Konto")
        label_konto.grid(row=3, column=0)
        def set_selected(choice):
            if choice == "Weiteres Konto hinzufügen":
                konto_popup = Popup_Konto()
                konto_popup.create_pop_up_konto(values=values_, parent_optionmenu=select_konto)

            if choice != "Wählen sie ein Konto" and choice != "Weiteres Konto hinzufügen":
                select_konto.configure(text_color="white")
        konten = get_konten()
        select_konto = customtkinter.StringVar(value="Wählen sie ein Konto")
        values_ = ["Wählen sie ein Konto"]
        values_.extend(konten)
        values_.append("Weiteres Konto hinzufügen")
        select_konto = customtkinter.CTkOptionMenu(master=add_buchung_fenster, values=values_, command=set_selected)
        select_konto.grid(row=3, column=1)
        select_konto.set("Wählen sie ein Konto")
########
        label_kategorien = customtkinter.CTkLabel(add_buchung_fenster, text="Kategorie")
        label_kategorien.grid(row=4, column=0)
        
        kategorien_combobox = customtkinter.CTkComboBox(master=add_buchung_fenster, values=["Test"])
        kategorien_combobox.grid(row=4, column=1)
        kategorien_combobox.set("Test")
########
        label_datum = customtkinter.CTkLabel(add_buchung_fenster, text="Datum")
        label_datum.grid(row=5, column=0)
########
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
                return check_

            if check() == True:
                
                add_buchung(
                            title=title.get(), 
                            wert=float(wert.get()),
                            buchungs_art=in_out.__contains__("+") ? "in":"out", # da die String in der Auswahl (aus Verständnissgründen) nicht der verarbeitbaren Strings entsprechen, werden sie hier umgewandelt
                            konto=konto_
                            )
                add_buchung_fenster.destroy()

        fertig_btn = customtkinter.CTkButton(add_buchung_fenster, command=finish_buchung)
        fertig_btn.grid(row=6, sticky="s", column=1)


def create_popup_buchung():
    this = Popup_Buchung()
    this.create_pop_up_buchung()
#############################################################################################################################
# erstellt ein Popup-Fenster, um ein Konto hinzuzufügen


class Popup_Konto():
    def create_pop_up_konto(self, values, parent_optionmenu):
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
            add_konto(name.get(), kontonummer.get())# <--- Fügt ein neues Konto des Konto-Dict zu, mit den Daten der Eingabefelder
            values.insert(len(values)-1, name.get())# <--- Akutalisiert die Kontoliste für das OptionMenus
            parent_optionmenu.configure(values=values)# <--- Aktualisiert das OptionMenu

            add_konto_fenster.destroy()                 # <--- Schließt das Popup-Fenster

        complete_button = customtkinter.CTkButton(master=add_konto_fenster, text="Konto hinzufügen", command=complete_add_konto)
        complete_button.grid(row=3)
