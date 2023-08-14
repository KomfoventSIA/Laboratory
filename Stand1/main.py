from GUI.MainWindow import MainWindow
from Measurements.Notification import Notification

##########
# Command to create .exe file:     pyinstaller --onefile --noconsole  main.py
##########

win = MainWindow()
win.create_main_window()


# notif = Notification()
