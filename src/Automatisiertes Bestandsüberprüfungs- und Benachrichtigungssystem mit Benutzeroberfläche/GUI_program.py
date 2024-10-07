import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem

# SQLite-Datenbankverbindung herstellen
def create_connection():
    connection = sqlite3.connect('Database_Projekt_Bestandsliste.db')
    return connection

# Funktion zum Laden des Inventars
def load_inventory():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT item_name, quantity FROM inventory")
    inventory = cursor.fetchall()
    connection.close()
    return inventory

# Funktion zum Laden der Benutzer
def load_users():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT username, password_hash, role FROM user")
    users = cursor.fetchall()
    connection.close()
    return users

# ... (andere Importe)
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem,QMainWindow

def open_main_program(role):
    global main_window
    print("Das Hauptprogramm wird geöffnet...")

    main_window = QMainWindow()
    main_window.setWindowTitle("Inventory Management")
    main_window.setGeometry(100, 100, 450, 350)

    # Tabs erstellen
    tabs = QTabWidget()

    # Tab für das Inventory
    inventory_tab = QWidget()
    inventory_layout = QVBoxLayout()
    
    # Zeige das Inventory
    inventory_list = QListWidget()
    inventory = load_inventory()
    for item in inventory:
        inventory_list.addItem(f"{item[0]}: {item[1]} Stück")
    inventory_layout.addWidget(inventory_list)
    inventory_tab.setLayout(inventory_layout)
    tabs.addTab(inventory_tab, "Inventory")

    # Tab für die Benutzerliste (nur für Admins)
    if role == 'Admin':
        user_tab = QWidget()
        user_layout = QVBoxLayout()

        # Tabelle für Benutzer
        user_table = QTableWidget()
        users = load_users()

        # Tabelle einrichten
        user_table.setColumnCount(3)
        user_table.setHorizontalHeaderLabels(["Benutzername", "Passwort", "Rolle"])
        user_table.setRowCount(len(users))

        for row, user in enumerate(users):
            user_table.setItem(row, 0, QTableWidgetItem(user[0]))  # Benutzername
            user_table.setItem(row, 1, QTableWidgetItem("*****"))  # Passwort maskieren
            user_table.setItem(row, 2, QTableWidgetItem(user[2]))  # Rolle

        # Button zum Anzeigen der Passwörter
        show_passwords_button = QPushButton("Passwörter anzeigen")
        show_passwords_button.clicked.connect(lambda: toggle_passwords(user_table, users))
        user_layout.addWidget(show_passwords_button)

        user_layout.addWidget(user_table)
        user_tab.setLayout(user_layout)
        tabs.addTab(user_tab, "Benutzer")

    main_window.setCentralWidget(tabs)
    main_window.show()

    print("Das Hauptprogramm wurde angezeigt.")  # Debugging-Ausgabe

def toggle_passwords(user_table, users):
    # Umschalten zwischen Passwort anzeigen und verbergen
    for row in range(len(users)):
        if user_table.item(row, 1).text() == "*****":
            # Passwort anzeigen
            user_table.setItem(row, 1, QTableWidgetItem(users[row][1].decode('utf-8')))  # Klartext
        else:
            # Passwort verbergen
            user_table.setItem(row, 1, QTableWidgetItem("*****"))  # Maskieren


