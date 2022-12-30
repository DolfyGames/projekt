import customtkinter
from data import get_buchungen
import popup

# erstellt die komplette Benutzeroberfläche


class Gui():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.existierende_objecte = {}

#########################################################################################################################################          
    # erstellt und aktualisiert die Buchungslistenansicht
    def set_update_buchungen(self):
        buchungen = list(get_buchungen())
        j=0

        for objects in self.existierende_objecte:
            self.existierende_objecte[objects].destroy()
            
        for buchung in buchungen:
            j+=1
            if buchung["buchungs_art"] == "in":
                    color = "#49705c"
            else:
                color = "#824e5e"
            self.existierende_objecte[j]= customtkinter.CTkFrame(self.frame1, fg_color=color,corner_radius=2)
            self.existierende_objecte[j].pack()
            buchungs_infos = customtkinter.CTkTextbox(self.existierende_objecte[j], width=450, height=60, fg_color="transparent")
            buchungs_infos.insert("0.0", buchung["title"]+"\n"+str(f'{buchung["wert"]:.2f}')+" €") #Quelle: https://bobbyhadz.com/blog/python-convert-float-to-string-with-precision

            buchungs_infos.configure(state="disabled")
            buchungs_infos.pack()
        print(self.existierende_objecte)
        
########################################################################################################################################

    def create_gui(self):
        # https://github.com/TomSchimansky/CustomTkinter dokumentation zu customtkiner
        # https://docs.python.org/3/library/tk.html dokumentation tkinter

        # erstellt ein Popup, um eine Buchung hinzuzufügen
        def add_buchung():
            this = popup.Popup_Buchung(parent=self)
            this.create_pop_up_buchung()



        # Standart konfiguration für das Fenster
        customtkinter.set_appearance_mode("System")
        app = customtkinter.CTk()
        app.geometry(self.width+"x"+self.height)

        # Standart Oberflächenitems
        frame = customtkinter.CTkFrame(app, width=500, height=500)
        frame.pack(pady=5)

        title = customtkinter.CTkLabel(frame, width=500, height=20, text="Buchungen")
        title.pack(pady=2, padx=2)

        self.frame1 = customtkinter.CTkFrame(frame, width=450, height=100)
        self.frame1.pack(pady=5)

        self.set_update_buchungen()
        add_button = customtkinter.CTkButton(frame, width=450, height=100, fg_color="#49705c", hover_color="#59886f", text="+", command=add_buchung)
        add_button.pack()

        # hiermit kann man das Programm schließen und man kann hier später auch noch eine Funktion zum Speichern aufrufen, bevor das Fenster geschlossen wird
        def disable_event():
            app.destroy()
        app.protocol("WM_DELETE_WINDOW", disable_event)


        #
        app.mainloop()