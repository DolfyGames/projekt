import customtkinter
from data import get_buchungen


class Gui():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buchungen = []
        self.buchung = []



    def create_gui(self):
        # https://github.com/TomSchimansky/CustomTkinter dokumentation zu customtkiner
        # https://docs.python.org/3/library/tk.html dokumentation tkinter

        def add_buchung():
            add_buchung = customtkinter.CTkToplevel()
            add_buchung.geometry("500x400")
            label = customtkinter.CTkLabel(add_buchung, text="Buchung hinzufügen")

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

        def set_update_buchungen():
            for i in self.buchungen:
                create_buchungs_gui(i)

        customtkinter.set_appearance_mode("System")
        app = customtkinter.CTk()
        app.geometry(self.width+"x"+self.height)


        frame = customtkinter.CTkFrame(app, width=500, height=500)
        frame.pack(pady=5)

        title = customtkinter.CTkLabel(frame,width=500, height=20, text="Buchungen")
        title.pack(pady=2,padx=2)

        frame1 = customtkinter.CTkFrame(frame, width=450, height=100)
        frame1.pack(pady=5)

        self.buchungen = get_buchungen()
        set_update_buchungen()

        add_button = customtkinter.CTkButton(frame1, width=450, height=100,fg_color="#49705c", hover_color="#59886f", text="+", command=add_buchung())
        add_button.pack()



        app.mainloop()


