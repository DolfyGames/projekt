import customtkinter
from data import get_buchungen
import popup

# erstellt die komplette Benutzeroberfläche 
class Gui():
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def create_gui(self):
        # https://github.com/TomSchimansky/CustomTkinter dokumentation zu customtkiner
        # https://docs.python.org/3/library/tk.html dokumentation tkinter

        # erstellt ein Popup, um eine Buchung hinzuzufügen
        def add_buchung():
            popup.create_popup_buchung()

        # erstellt die ganzen Buchungen als Listenansicht
        def create_buchungs_gui(buchung_):
            if buchung_["buchungs_art"] == "in":
                color = "#49705c"
            else:
                color = "#824e5e"
            frame_ = customtkinter.CTkFrame(frame1, fg_color=color)
            frame_.pack()
            title_ = customtkinter.CTkTextbox(frame_, width=450, height=20, fg_color="transparent")
            title_.insert("0.0", buchung_["title"])
            title_.configure(state="disabled")
            title_.pack()
        # aktualisiert die Buchungslistenansicht
        def set_update_buchungen():
            for i in self.buchungen:
                create_buchungs_gui(i)

        # Standart konfiguration für das Fenster
        customtkinter.set_appearance_mode("System")
        app = customtkinter.CTk()
        app.geometry(self.width+"x"+self.height)

        # Standart Oberflächenitems 
        frame = customtkinter.CTkFrame(app, width=500, height=500)
        frame.pack(pady=5)

        title = customtkinter.CTkLabel(frame,width=500, height=20, text="Buchungen")
        title.pack(pady=2,padx=2)

        frame1 = customtkinter.CTkFrame(frame, width=450, height=100)
        frame1.pack(pady=5)

        self.buchungen = get_buchungen()
        set_update_buchungen()

        add_button = customtkinter.CTkButton(frame1, width=450, height=100,fg_color="#49705c", hover_color="#59886f", text="+", command=add_buchung)
        add_button.pack()


        # hiermit kann man das Programm schließen und man kann hier später auch noch eine Funktion zum Speichern aufrufen, bevor das Fenster geschlossen wird
        def disable_event():
            app.destroy()
        app.protocol("WM_DELETE_WINDOW", disable_event)

        # 
        app.mainloop()


