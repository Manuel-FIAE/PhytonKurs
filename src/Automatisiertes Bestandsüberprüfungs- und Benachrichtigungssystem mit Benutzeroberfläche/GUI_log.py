import sys
import sqlite3
import bcrypt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import re  # Für Passwort-Richtlinien

# Importiere die Funktion aus GUI_program.py
from GUI_program import open_main_program  # Nur die Funktion importieren

# SQLite-Datenbankverbindung ohne Tabellenerstellung
def create_connection():
    connection = sqlite3.connect('Database_Projekt_Bestandsliste.db')  # Dein Datenbankname
    return connection

# Passwort-Richtlinien überprüfen
def validate_password(password):
    if len(password) < 8:
        return False, "Passwort muss mindestens 8 Zeichen lang sein."
    if not re.search("[A-Z]", password):
        return False, "Passwort muss mindestens einen Großbuchstaben enthalten."
    if not re.search("[a-z]", password):
        return False, "Passwort muss mindestens einen Kleinbuchstaben enthalten."
    if not re.search("[0-9]", password):
        return False, "Passwort muss mindestens eine Zahl enthalten."
    return True, "Passwort ist gültig."

# Registrierung - Benutzer hinzufügen
def register_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()

    # Überprüfen, ob der Benutzername bereits existiert
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    if cursor.fetchone():
        return False, "Benutzername existiert bereits."

    # Passwort-Richtlinien überprüfen
    valid, message = validate_password(password)
    if not valid:
        return False, message

    # Passwort hashen
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Neuen Benutzer hinzufügen
    cursor.execute("INSERT INTO user (username, password_hash, role) VALUES (?, ?, ?)", (username, hashed_password, 'User'))
    connection.commit()
    connection.close()
    return True, "Registrierung erfolgreich!"

# Fenster für Registrierung erstellen (neuen Benutzer hinzufügen)
class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Neuen Benutzer registrieren")
        self.setGeometry(200, 200, 400, 200)

        # Layout für das Registrierungsfenster
        layout = QVBoxLayout()

        # Benutzername und Passwort Felder
        self.label_username = QLabel("Benutzername:")
        self.input_username = QLineEdit()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)

        self.label_password = QLabel("Passwort:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        # Registrierung-Button
        self.register_button = QPushButton("Benutzer hinzufügen")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        # Setze das Layout für das Fenster
        self.setLayout(layout)

    def register(self):
        username = self.input_username.text()
        password = self.input_password.text()

        # Registrierung versuchen
        success, message = register_user(username, password)
        msg = QMessageBox()
        if success:
            msg.setIcon(QMessageBox.Information)
            msg.setText(message)
        else:
            msg.setIcon(QMessageBox.Warning)
            msg.setText(message)
        msg.exec_()

# Admin-Login-Fenster (wird aufgerufen, wenn auf "Registrieren" geklickt wird)
class AdminLoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin-Login")
        self.setGeometry(200, 200, 400, 150)

        # Layout für das Admin-Login-Fenster
        layout = QVBoxLayout()

        self.label_username = QLabel("Admin-Benutzername:")
        self.input_username = QLineEdit()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)

        self.label_password = QLabel("Admin-Passwort:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        # Login-Button
        self.login_button = QPushButton("Anmelden")
        self.login_button.clicked.connect(self.admin_login)
        layout.addWidget(self.login_button)

        # Setze das Layout für das Fenster
        self.setLayout(layout)

    def admin_login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        connection = create_connection()
        cursor = connection.cursor()

        # Überprüfen, ob der Benutzer ein Admin ist
        cursor.execute("SELECT password_hash, role FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            hashed_password = result[0]
            role = result[1]

            # Passwort validieren und Rolle überprüfen
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password) and role == 'Admin':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Admin-Login erfolgreich!")
                msg.exec_()
                self.accept()  # Schließt das Admin-Login-Fenster und gibt Kontrolle zurück
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Falsches Passwort oder keine Admin-Rechte.")
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Admin-Benutzername nicht gefunden.")
            msg.exec_()

# Hauptanwendung
app = QApplication(sys.argv)

# Fenster erstellen
window = QWidget()
window.setWindowTitle("Bestands- und Benachrichtigungssystem")
window.setGeometry(100, 100, 600, 400)
window.setWindowIcon(QIcon('logo.jpg'))  # Setze ein Fenster-Icon, wenn gewünscht

# Layout erstellen
layout = QVBoxLayout()

# Programmnamen anzeigen
program_name = QLabel("Bestands- und Benachrichtigungssystem")
program_name.setStyleSheet("font-size: 22px; font-weight: bold; text-align: center;")
program_name.setAlignment(Qt.AlignCenter)
layout.addWidget(program_name)

# Logo hinzufügen
logo = QLabel()
pixmap = QPixmap("src/Automatisiertes Bestandsüberprüfungs- und Benachrichtigungssystem mit Benutzeroberfläche/logo.jpg")  # Pfad zu deinem Logo anpassen
scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
logo.setPixmap(scaled_pixmap)
logo.setAlignment(Qt.AlignCenter)
layout.addWidget(logo)

# Login-Felder
login_layout = QVBoxLayout()

# Benutzername
username_layout = QHBoxLayout()
label_username = QLabel("Benutzername:")
input_username = QLineEdit()
input_username.setMaxLength(14)
input_username.setFixedWidth(150)
username_layout.addWidget(label_username)
username_layout.addWidget(input_username)
login_layout.addLayout(username_layout)

# Passwort
password_layout = QHBoxLayout()
label_password = QLabel("Passwort:")
input_password = QLineEdit()
input_password.setMaxLength(14)
input_password.setFixedWidth(150)
input_password.setEchoMode(QLineEdit.Password)  # Passwort verstecken
password_layout.addWidget(label_password)
password_layout.addWidget(input_password)
login_layout.addLayout(password_layout)

layout.addLayout(login_layout)

def login():
    username = input_username.text()
    password = input_password.text()
    connection = create_connection()
    cursor = connection.cursor()

    # Benutzer anhand des Benutzernamens finden
    cursor.execute("SELECT password_hash, role FROM user WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result:
        hashed_password = result[0]
        role = result[1]

        # Passwort validieren
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"Login erfolgreich! Rolle: {role}")
            msg.exec_()

            # Debugging: Prüfen, ob diese Zeile erreicht wird
            print(f"Login erfolgreich für {username} mit Rolle {role}")

            # Schließe das aktuelle Login-Fenster
            window.close()

            # Öffne das Hauptfenster
            open_main_program(role)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Falsches Passwort.")
            msg.exec_()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Benutzername nicht gefunden.")
        msg.exec_()


# Login Bestätigen mit Enter
input_password.returnPressed.connect(login)

# Registrierung-Button im Hauptfenster
sign_in_label = QLabel("<a href='#'>Registrieren</a>")
sign_in_label.setStyleSheet("color: blue; text-decoration: underline;")
sign_in_label.setOpenExternalLinks(False)

# Funktion, um das Admin-Login-Fenster zu öffnen
def open_admin_login_window():
    admin_login_window = AdminLoginWindow()
    if admin_login_window.exec_() == QDialog.Accepted:  # Wenn der Admin-Login erfolgreich ist
        register_window = RegisterWindow()  # Öffne das Registrierungsfenster
        register_window.exec_()

sign_in_label.mousePressEvent = lambda event: open_admin_login_window()  # Klickbare Registrierung
layout.addWidget(sign_in_label, alignment=Qt.AlignCenter)

# Layout auf Fenster anwenden
window.setLayout(layout)

# Fenster anzeigen
window.show()

# Hauptanwendung starten
sys.exit(app.exec_())
