import customtkinter
import popup
from PIL import Image
import tkinter as tk
# erstellt die komplette Benutzeroberfläche


class Gui():
    def __init__(self, width, height, datamanager):
        self.width = width
        self.height = height
        self.existierende_objecte = {}
        self.datamanager = datamanager

#########################################################################################################################################          
    # erstellt und aktualisiert die Buchungslistenansicht
    def set_update_buchungen(self):
        buchungen = list(self.datamanager.get_buchungen())
        j=0

        for objects in self.existierende_objecte:
            self.existierende_objecte[objects].destroy()
            
        for buchung in buchungen:

            if buchung["buchungs_art"] == "in":
                    color = "green"
            else:
                color = "red"

            def edit(buchung_ = buchung):
                edit_popup = popup.Popup_Buchung(datamanager=self.datamanager,buchung=buchung_)
                edit_popup.create_pop_up_buchung()

            self.existierende_objecte[j]= customtkinter.CTkFrame(self.frame1, fg_color=color,corner_radius=2)
            self.existierende_objecte[j].pack(padx=2,pady=2)
            buchungs_infos = customtkinter.CTkTextbox(self.existierende_objecte[j], width=450, height=80, fg_color="transparent")
            buchungs_infos.insert("0.0", buchung["title"]+"\n\n"+"Wert: "+str(f'{buchung["wert"]:.2f}')+" €"+"             "+"Konto: "+buchung["konto"]+"              "+"Datum: "+buchung["zeitpunkt"]+"\n"+"Kategorien: "+ '; '.join(buchung["kategorie"])) #Quelle: https://bobbyhadz.com/blog/python-convert-float-to-string-with-precision

            buchungs_infos.configure(state="disabled")
            buchungs_infos.grid(row=0,column=0,padx=2,pady=2)

            edit_btn = {}

            zahnrad = customtkinter.CTkImage(dark_image=Image.open("edit.png"),size=(30,30))
            edit_btn[j] = customtkinter.CTkButton(self.existierende_objecte[j], width=80, height=80, image=zahnrad, fg_color="transparent",text="", command=edit)
            edit_btn[j].grid(row=0,column=1,padx=2,pady=2)
            j+=1
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
########################################################################################################################################
    def set_update_kontostand(self):
        self.kontostand_.set(str(f'{self.datamanager.get_kontostand():.2f}'+" €"))
        if self.datamanager.get_kontostand()>0:
            color = "green"
        elif self.datamanager.get_kontostand()<0:
            color="red"
        else:
            color="white"
        
        
        self.kontostand.configure(text_color=color)
#########################################################################################################################################
    def set_update_filter(self):
        konten = self.datamanager.get_konten()
        kategorien = self.datamanager.get_kategorien()
        filter_checkbox = {}
        filter_val = {}
        j = 2 #  n um die Checkboxen in die passenden Zeilen zu packen
        filtern_label_konten = customtkinter.CTkLabel(self.filtern,text="Konten")
        filtern_label_konten.grid(row=1,column=0,padx=5,pady=5)
        for i in konten:
            def checked(val=i["name"], j_=j):
                self.datamanager.filtern(key=val, state=filter_val[j_].get())
            
            filter_val[j] = customtkinter.BooleanVar()
            filter_checkbox[j] = customtkinter.CTkCheckBox(self.filtern,text=i["name"],command=checked, variable=filter_val[j], onvalue=True, offvalue=False)
            filter_checkbox[j].grid(row=j,column=0, padx=5,pady=2) # + n um die Checkboxen in die passenden Zeilen zu packen
            j += 1
            
        filtern_label_kategorien = customtkinter.CTkLabel(self.filtern,text="Kategorien")
        filtern_label_kategorien.grid(row=j,column=0,padx=5,pady=5)
        j+=1
        for i in kategorien:
            def checked(val=i, j_=j):
                self.datamanager.filtern(key=val, state=filter_val[j_].get())
            
            filter_val[j] = customtkinter.BooleanVar()
            filter_checkbox[j] = customtkinter.CTkCheckBox(self.filtern,text=i,command=checked, variable=filter_val[j], onvalue=True, offvalue=False)
            filter_checkbox[j].grid(row=j+2,column=0, padx=5,pady=2) # + n um die Checkboxen in die passenden Zeilen zu packen
            j += 1
#########################################################################################################################################
        
    
    def create_gui(self):
        # https://github.com/TomSchimansky/CustomTkinter dokumentation zu customtkiner
        # https://docs.python.org/3/library/tk.html dokumentation tkinter

        # erstellt ein Popup, um eine Buchung hinzuzufügen
        def add_buchung():
            this = popup.Popup_Buchung(datamanager=self.datamanager)
            this.create_pop_up_buchung()



        # Standart konfiguration für das Fenster
        customtkinter.set_appearance_mode("System")
        app = customtkinter.CTk()
        app.geometry(self.width+"x"+self.height)
        app.title("Abrechnungstool")

        app.grid_rowconfigure(0, weight=1)

        sidepanel = customtkinter.CTkFrame(master=app)
        sidepanel.grid(row=0,column=0,padx=10,pady=10, sticky="nsew")
        sidepanel.grid_rowconfigure((0,1),weight=1)
#####        
        sortieren = customtkinter.CTkFrame(master=sidepanel)
        sortieren.grid(row=0,column=0,padx=5,pady=5,sticky="nsew")
        sort_label = customtkinter.CTkLabel(sortieren,text="Sortieren nach: ")
        sort_label.grid(row=0,column=0,padx=5,pady=5)
        
        select_var = customtkinter.StringVar()
        self.is_selected = ""
        def clicked():
        # je nach angeklickten radiobutton werden die Buchungen danach dem kriterium sortiert    
            val = select_var.get()
            if val != self.is_selected:
                self.is_selected = val
                if val == "wert_auf":
                    self.datamanager.sort("wert",False)
                elif val == "wert_ab":
                    self.datamanager.sort("wert",True)
                elif val == "neu":
                    self.datamanager.sort("zeitpunkt",True)
                else:
                    self.datamanager.sort("zeitpunkt",False)
            else:
                self.datamanager.sort("off",False)
                select_var.set("")
        
        sort_label_wert = customtkinter.CTkLabel(sortieren,text="Wert: ")
        sort_label_wert.grid(row=1,column=0)
        wert_aufsteigend = customtkinter.CTkRadioButton(sortieren,text="Aufstiegend",variable=select_var,value="wert_auf", command=clicked)
        wert_aufsteigend.grid(row=1,column=1)
        
        wert_absteigend = customtkinter.CTkRadioButton(sortieren,text="Abtiegend",variable=select_var,value="wert_ab", command=clicked)
        wert_absteigend.grid(row=1,column=2)
        
        sort_label_datum = customtkinter.CTkLabel(sortieren,text="Datum")
        sort_label_datum.grid(row=2,column=0)
        datum_neu = customtkinter.CTkRadioButton(sortieren,text="Neu->Alt",variable=select_var,value="neu", command=clicked)
        datum_neu.grid(row=2,column=1)
        datum_alt = customtkinter.CTkRadioButton(sortieren,text="Alt->Neu",variable=select_var,value="alt", command=clicked)
        datum_alt.grid(row=2,column=2)
#####
        self.filtern = customtkinter.CTkFrame(master=sidepanel)
        self.filtern.grid(row=1,column=0,padx=5,pady=5, sticky="nsew")
        filtern_label = customtkinter.CTkLabel(self.filtern,text="Filter")
        filtern_label.grid(row=0,column=0,padx=5,pady=5)

        self.set_update_filter()
#####
        finanz_übersicht =  customtkinter.CTkFrame(master=app,height=1060,width=700)
        finanz_übersicht.grid(row=0,column=1,padx=10,pady=10, sticky="nsew")
        finanz_übersicht.grid_rowconfigure(1,weight=1)
        
        tool_frame =  customtkinter.CTkFrame(master=finanz_übersicht)
        tool_frame.grid(row=0,column=0, sticky="nsew", padx=5, pady=5)
        
        tool_label = customtkinter.CTkLabel(tool_frame,text="Kontostand: Gesammt")
        tool_label.grid(row=0,column=0)
        self.kontostand_ = customtkinter.StringVar()
        self.kontostand = customtkinter.CTkEntry(tool_frame,state="disabled",textvariable=self.kontostand_)
        self.kontostand.grid(row=1,column=0, columnspan=1, padx=5,pady=5)

        def suche(value):
            such_wert = value
            if value !="Suche" and value != "":
                self.datamanager.filtern(state=True, key=such_wert, such_filter=True)
            else:
                if hasattr(self,"frame1"):
                    self.datamanager.filtern(state=False, such_filter=False)
            return True

        suche = tool_frame.register(suche)
        tool_suche = customtkinter.CTkEntry(master=tool_frame, placeholder_text="Suche",validate="key", validatecommand= (suche, '%P'))
        tool_suche.grid(row=1, column=1,padx=5,pady=5)

        self.set_update_kontostand()

                
        # Standart Oberflächenitems
        frame = customtkinter.CTkFrame(finanz_übersicht)
        frame.grid(row=1,column=0,pady=10, padx=5, sticky="nsew")
        frame.grid_rowconfigure(1, weight =1)
        title = customtkinter.CTkLabel(frame, text="Buchungen")
        title.grid(row=0,column=0,pady=2, padx=2)

        def set_scrollregion(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        self.canvas = customtkinter.CTkCanvas(frame, height= 700,width=534,bg="#000000", bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid(row=1, column=0,padx=5,pady=5,sticky="nsew")
        self.canvas.bind("<Configure>", set_scrollregion)
        self.frame1 = customtkinter.CTkFrame(self.canvas, width=534)
        self.frame1.grid(row=0, column=0,padx=5,pady=5,sticky="nsew")
        self.canvas.create_window((0,0),window=self.frame1,anchor="nw")
        scrollbar = customtkinter.CTkScrollbar(frame,command=self.canvas.yview)
        scrollbar.grid(row=1,column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        
        self.set_update_buchungen()
        add_button = customtkinter.CTkButton(frame, fg_color="#49705c", hover_color="#59886f", text="+", command=add_buchung)
        add_button.grid(row=2, column=0, padx=5,pady=5)

        # hiermit kann man das Programm schließen und man kann hier später auch noch eine Funktion zum Speichern aufrufen, bevor das Fenster geschlossen wird
        def disable_event():
            self.datamanager.save()
            app.destroy()
        app.protocol("WM_DELETE_WINDOW", disable_event)


        #
        app.mainloop()