import customtkinter
from data import get_buchungen, get_kontostand
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
                    color = "green"
            else:
                color = "red"
            self.existierende_objecte[j]= customtkinter.CTkFrame(self.frame1, fg_color=color,corner_radius=2)
            self.existierende_objecte[j].pack(padx=2,pady=2)
            buchungs_infos = customtkinter.CTkTextbox(self.existierende_objecte[j], width=450, height=80, fg_color="transparent")
            buchungs_infos.insert("0.0", buchung["title"]+"\n\n"+"Wert: "+str(f'{buchung["wert"]:.2f}')+" €"+"             "+"Konto: "+buchung["konto"]+"              "+"Datum: "+buchung["zeitpunkt"]) #Quelle: https://bobbyhadz.com/blog/python-convert-float-to-string-with-precision

            buchungs_infos.configure(state="disabled")
            buchungs_infos.pack(padx=2,pady=2)
        print(self.existierende_objecte)
        
########################################################################################################################################
    def set_update_kontostand(self):
        self.kontostand_.set(str(f'{get_kontostand():.2f}'+" €"))
        if get_kontostand()>0:
            color = "green"
        elif get_kontostand()<0:
            color="red"
        else:
            color="white"
        
        
        self.kontostand.configure(text_color=color)

        
    
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
        app.title("Abrechnungstool")
        
        sidepanel = customtkinter.CTkFrame(master=app, height=1060,width=350)
        sidepanel.grid(row=0,column=0,padx=10,pady=10)

        finanz_übersicht =  customtkinter.CTkFrame(master=app,height=1060,width=700)
        finanz_übersicht.grid(row=0,column=1,padx=10,pady=10)
        
        tool_frame =  customtkinter.CTkFrame(master=finanz_übersicht)
        tool_frame.grid(row=0,column=0) 
        
        tool_label = customtkinter.CTkLabel(tool_frame,text="Kontostand: Gesammt")
        tool_label.grid(row=0,column=0)
        self.kontostand_ = customtkinter.StringVar()
        self.kontostand = customtkinter.CTkEntry(tool_frame,state="disabled",textvariable=self.kontostand_)
        self.kontostand.grid(row=1,column=0, columnspan=1)

        self.set_update_kontostand()

                
        # Standart Oberflächenitems
        frame = customtkinter.CTkFrame(finanz_übersicht)
        frame.grid(row=1,column=0,pady=10, padx=10)

        title = customtkinter.CTkLabel(frame, text="Buchungen")
        title.pack(pady=2, padx=2)

        self.frame1 = customtkinter.CTkFrame(frame )
        self.frame1.pack(pady=5)

        self.set_update_buchungen()
        add_button = customtkinter.CTkButton(frame, fg_color="#49705c", hover_color="#59886f", text="+", command=add_buchung)
        add_button.pack()

        # hiermit kann man das Programm schließen und man kann hier später auch noch eine Funktion zum Speichern aufrufen, bevor das Fenster geschlossen wird
        def disable_event():
            app.destroy()
        app.protocol("WM_DELETE_WINDOW", disable_event)


        #
        app.mainloop()