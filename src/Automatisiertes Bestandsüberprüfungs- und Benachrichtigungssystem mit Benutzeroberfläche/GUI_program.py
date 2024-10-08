import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem, QMainWindow, QLineEdit, QLabel, QHBoxLayout, QMessageBox, QApplication
from PyQt5.QtCore import Qt

# SQLite-Datenbankverbindung herstellen
def create_connection():
    connection = sqlite3.connect('Database_Projekt_Bestandsliste.db')
    return connection

def validate_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT password_hash, role FROM user WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result:
        stored_password, role = result
        if password == stored_password:
            return True, role
    connection.close()
    return False, None

# Funktion zum Laden des Inventars
def load_inventory():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT inventory_id, item_name, quantity, threshold FROM inventory")
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

# Angepasste Funktion zum Filtern von Artikeln, die bestellt werden müssen (Menge < Grenzwert) - jetzt mit ID
def load_items_below_threshold():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT inventory_id, item_name, quantity, threshold FROM inventory WHERE quantity < threshold")
    items_below_threshold = cursor.fetchall()
    connection.close()
    return items_below_threshold

# Funktion zum Senden der E-Mail mit schöner Formatierung und Artikel-ID
def send_email(items_below_threshold):
    sender_email = "manu-panu@gmx.de"  # Deine GMX-E-Mail-Adresse
    receiver_email = "perrotti1811@gmx.de"  # Empfänger E-Mail-Adresse
    password = "fdfsdf"  # Dein GMX-Passwort oder App-Passwort

    smtp_server = "mail.gmx.net"
    smtp_port = 587

    subject = "Bestellliste: Artikel unter dem Grenzwert"

    # Schöner formulierte Nachricht mit einer Tabelle, die die Artikel-ID enthält
    body = """
    Sehr geehrte Damen und Herren,<br><br>

    im Folgenden finden Sie eine Liste der Artikel, die derzeit unter dem festgelegten Grenzwert liegen und dringend nachbestellt werden sollten:<br><br>

    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>ID</th>
            <th>Artikelname</th>
            <th>Stückzahl</th>
            <th>Grenzwert</th>
        </tr>
    """

    for item in items_below_threshold:
        body += f"""
        <tr>
            <td>{item[0]}</td>
            <td>{item[1]}</td>
            <td>{item[2]}</td>
            <td>{item[3]}</td>
        </tr>
    """

    body += """
    </table><br><br>

    Bitte prüfen Sie die Bestände und veranlassen Sie zeitnah eine Nachbestellung.<br><br>

    Mit freundlichen Grüßen,<br><br>
    Ihr Bestandsmanagement-Team<br>
    Manuel Perrotta
    """

    # E-Mail Nachricht zusammensetzen
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))  # HTML für die Tabelle verwenden

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {e}")

# Funktion zum Senden der E-Mail bei Login
def email_on_login():
    items_below_threshold = load_items_below_threshold()
    if items_below_threshold:
        send_email(items_below_threshold)

# Funktion zum Hinzufügen von Artikeln
def add_item(item_name, quantity, threshold, inventory_table, grenz_table):
    if item_name and quantity and threshold:
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO inventory (item_name, quantity, threshold) VALUES (?, ?, ?)", (item_name, quantity, threshold))
            connection.commit()
            connection.close()
            update_inventory_table(inventory_table)
            update_orders_table(grenz_table)
            email_on_change()  # E-Mail senden, wenn Artikel geändert werden
        except Exception as e:
            print(f"Fehler beim Hinzufügen des Artikels: {e}")

# Funktion zum Bearbeiten von Artikeln (nur die Menge wird aktualisiert)
def update_item(item_id, new_quantity, inventory_table, grenz_table):
    if item_id and new_quantity:
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE inventory SET quantity = ? WHERE inventory_id = ?", (new_quantity, item_id))
            connection.commit()
            connection.close()
            update_inventory_table(inventory_table)
            update_orders_table(grenz_table)
            email_on_change()  # E-Mail senden, wenn Artikel geändert werden
        except Exception as e:
            print(f"Fehler beim Bearbeiten des Artikels: {e}")

# Funktion zum Löschen von Artikeln
def delete_item(item_id, inventory_table, grenz_table):
    if item_id:
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM inventory WHERE inventory_id = ?", (item_id,))
            connection.commit()
            connection.close()
            update_inventory_table(inventory_table)
            update_orders_table(grenz_table)
            email_on_change()  # E-Mail senden, wenn Artikel geändert werden
        except Exception as e:
            print(f"Fehler beim Löschen des Artikels: {e}")

# Funktion zum Löschen von Benutzern
def delete_user(username, user_table):
    if username:
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM user WHERE username = ?", (username,))
            connection.commit()
            connection.close()
            update_user_table(user_table)
        except Exception as e:
            print(f"Fehler beim Löschen des Benutzers: {e}")

# Funktion zum Überprüfen und Senden von E-Mails bei Bestandsänderungen
def email_on_change():
    items_below_threshold = load_items_below_threshold()
    if items_below_threshold:
        send_email(items_below_threshold)

# Hauptfenster mit GUI
def open_main_program(role):
    global main_window

    main_window = QMainWindow()
    main_window.setWindowTitle("Inventory Management")
    main_window.setGeometry(100, 100, 600, 400)

    # Tabs erstellen
    tabs = QTabWidget()

    # Tab für das Inventory
    inventory_tab = QWidget()
    inventory_layout = QVBoxLayout()

    # Tabelle für Inventory
    inventory_table = QTableWidget()
    inventory_table.setColumnCount(4)
    inventory_table.setHorizontalHeaderLabels(["ID", "Produkt", "Stückzahl", "Grenzwert"])
    update_inventory_table(inventory_table)

    inventory_layout.addWidget(inventory_table)
    inventory_tab.setLayout(inventory_layout)
    tabs.addTab(inventory_tab, "Inventory")

    # Tab für Bestellungen (Artikel unter Grenzwert)
    grenz_tab = QWidget()
    grenz_layout = QVBoxLayout()

    # Tabelle für Artikel unter dem Grenzwert
    grenz_table = QTableWidget()
    grenz_table.setColumnCount(4)
    grenz_table.setHorizontalHeaderLabels(["ID", "Produkt", "Stückzahl", "Grenzwert"])
    update_orders_table(grenz_table)

    grenz_layout.addWidget(grenz_table)
    grenz_tab.setLayout(grenz_layout)
    tabs.addTab(grenz_tab, "Bestellungen")

    # Tab für die Benutzerliste (nur für Admins)
    if role == 'Admin':
        user_tab = QWidget()
        user_layout = QVBoxLayout()

        # Tabelle für Benutzer
        user_table = QTableWidget()
        user_table.setColumnCount(3)
        user_table.setHorizontalHeaderLabels(["Benutzername", "Passwort", "Rolle"])
        update_user_table(user_table)

        user_layout.addWidget(user_table)
        user_tab.setLayout(user_layout)
        tabs.addTab(user_tab, "Benutzer")

        # Tab für das Löschen von Benutzern
        loeschen_tab = QWidget()
        loeschen_layout = QVBoxLayout()
        
        username_input = QLineEdit()
        username_input.setPlaceholderText("Benutzername zum Löschen")
        loeschen_layout.addWidget(username_input)

        delete_user_button = QPushButton("Benutzer löschen")
        delete_user_button.clicked.connect(lambda: delete_user(username_input.text(), user_table))
        loeschen_layout.addWidget(delete_user_button)

        loeschen_tab.setLayout(loeschen_layout)
        tabs.addTab(loeschen_tab, "Benutzer löschen")

    # Tab für die Artikelverwaltung (Hinzufügen, Bearbeiten, Löschen)
    option_tab = QWidget()
    option_layout = QVBoxLayout()

    add_item_layout = QVBoxLayout()
    header_label = QLabel("Artikelverwaltung")
    header_label.setStyleSheet("font-weight: bold; font-size: 18px;")
    add_item_layout.addWidget(header_label, alignment=Qt.AlignLeft)

    item_id_input = QLineEdit()
    item_id_input.setPlaceholderText("Artikel-ID (für Bearbeiten/Löschen)")
    add_item_layout.addWidget(item_id_input)

    item_name_input = QLineEdit()
    item_name_input.setPlaceholderText("Artikelname")
    add_item_layout.addWidget(item_name_input)

    item_quantity_input = QLineEdit()
    item_quantity_input.setPlaceholderText("Stückzahl")
    add_item_layout.addWidget(item_quantity_input)

    item_threshold_input = QLineEdit()
    item_threshold_input.setPlaceholderText("Grenzwert (nur beim Hinzufügen)")
    add_item_layout.addWidget(item_threshold_input)

    add_item_button = QPushButton("Artikel hinzufügen")
    add_item_button.clicked.connect(lambda: add_item(item_name_input.text(), item_quantity_input.text(), item_threshold_input.text(), inventory_table, grenz_table))
    
    update_item_button = QPushButton("Artikel bearbeiten (Menge)")
    update_item_button.clicked.connect(lambda: update_item(item_id_input.text(), item_quantity_input.text(), inventory_table, grenz_table))
    
    delete_item_button = QPushButton("Artikel löschen")
    delete_item_button.clicked.connect(lambda: delete_item(item_id_input.text(), inventory_table, grenz_table))

    button_layout = QHBoxLayout()
    button_layout.addWidget(add_item_button)
    button_layout.addWidget(update_item_button)
    button_layout.addWidget(delete_item_button)
    
    add_item_layout.addLayout(button_layout)
    option_layout.addLayout(add_item_layout)
    option_tab.setLayout(option_layout)
    tabs.addTab(option_tab, "Artikelverwaltung")

    main_window.setCentralWidget(tabs)
    main_window.show()

# Funktion zum Aktualisieren der Inventarliste in der GUI
def update_inventory_table(inventory_table):
    inventory = load_inventory()
    inventory_table.setRowCount(len(inventory))
    for row, item in enumerate(inventory):
        inventory_table.setItem(row, 0, QTableWidgetItem(str(item[0])))  # ID
        inventory_table.setItem(row, 1, QTableWidgetItem(item[1]))  # Produktname
        inventory_table.setItem(row, 2, QTableWidgetItem(str(item[2])))  # Stückzahl
        inventory_table.setItem(row, 3, QTableWidgetItem(str(item[3])))  # Grenzwert

# Funktion zum Aktualisieren der Benutzerliste in der GUI
def update_user_table(user_table):
    users = load_users()
    user_table.setRowCount(len(users))
    for row, user in enumerate(users):
        user_table.setItem(row, 0, QTableWidgetItem(user[0]))  # Benutzername
        user_table.setItem(row, 1, QTableWidgetItem("*****"))  # Passwort maskieren
        user_table.setItem(row, 2, QTableWidgetItem(user[2]))  # Rolle

# Funktion zum Aktualisieren der Bestellungen (Artikel unter Grenzwert) in der GUI und E-Mail senden bei Änderungen
def update_orders_table(grenz_table):
    items_below_threshold = load_items_below_threshold()  # Artikel unter Grenzwert laden
    grenz_table.setRowCount(len(items_below_threshold))
    
    for row, item in enumerate(items_below_threshold):
        grenz_table.setItem(row, 0, QTableWidgetItem(str(item[0])))  # ID
        grenz_table.setItem(row, 1, QTableWidgetItem(item[1]))  # Produktname
        grenz_table.setItem(row, 2, QTableWidgetItem(str(item[2])))  # Stückzahl
        grenz_table.setItem(row, 3, QTableWidgetItem(str(item[3])))  # Grenzwert

    # E-Mail senden, wenn sich etwas ändert
    email_on_change()
    
# Funktion zum Login-Prozess
def handle_login(username, password):
    success, role = validate_user(username, password)
    
    if success:
        QMessageBox.information(None, "Erfolgreich", "Login erfolgreich!")

        # E-Mail wird nach dem erfolgreichen Login gesendet
        email_on_login()

        # Öffne das Hauptprogramm
        open_main_program(role)
    else:
        QMessageBox.warning(None, "Fehlgeschlagen", "Benutzername oder Passwort falsch.")