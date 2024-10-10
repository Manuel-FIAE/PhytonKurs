import sys
from PyQt5.QtWidgets import QApplication
from GUI_log import show_login_window

# Starte die Anwendung mit dem Login-Fenster
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Erstelle eine QApplication
    show_login_window()           # Zeige das Login-Fenster
    sys.exit(app.exec_())         # Starte die Event-Schleife
