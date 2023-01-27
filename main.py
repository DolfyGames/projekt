import gui
import data

# Hinweis: Das ganze Programm ist in feinstem Denglisch,
# das liegt daran, dass ich das Programm eigentlich in Deutsch schreiben wollte, allerings sind manche Deutsche begriffe lang und komisch :D
# Und ganz in Englisch hab ich es auch nicht geschrieben, da ich manche englische Begriffe nicht weis und auch keine lust hatte die immer nachzuschauen 
datamanager = data.Data()       # erstellt den Datenmanager (welche das ganze "backend" übernimmt)
datamanager.load()
gui_ = gui.Gui("1920","1080",datamanager) # erstellt die benutzeroberfläche 
datamanager.set_gui(gui_)  # übergibt dem datenmanager die classe der benutzeroberfläche, sodass dieser dann teile der Benutzeroberfläche aktualisieren lassen kann 
gui_.create_gui()

