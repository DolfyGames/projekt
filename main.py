import gui
import data

# Hinweis: Das ganze Programm ist in feinstem Denglisch,
# das liegt daran, dass ich das Programm eigentlich in Deutsch schreiben wollte, allerings sind manche Deutsche begriffe lang und komisch :D
# Und ganz in Englisch hab ich es auch nicht geschrieben, da ich manche englische Begriffe nicht weis und auch keine lust hatte die immer nachzuschauen 
datamanager = data.Data()
datamanager.load()
gui_ = gui.Gui("1920","1080",datamanager)
datamanager.set_gui(gui_)
gui_.create_gui()

