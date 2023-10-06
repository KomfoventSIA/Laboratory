from GUI.MainWindow import MainWindow
from Measurements.Notification import Notification

##########
# Command to create .exe file:     pyinstaller --onefile --noconsole  main.py
##########

win = MainWindow(stand='Stand Nr.2')   # available parameters: 'Stand Nr.1'; 'Stand Nr.2'
win.create_main_window()


# notif = Notification()
