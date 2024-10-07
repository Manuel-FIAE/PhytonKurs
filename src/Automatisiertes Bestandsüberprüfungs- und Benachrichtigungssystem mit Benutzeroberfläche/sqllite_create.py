import sqlite3
import bcrypt

# Verbindung zur SQLite-Datenbank herstellen
def create_database():
    conn = sqlite3.connect("Database_Projekt_Bestandsliste.db")
    cur = conn.cursor()

    # SQL-Abfragen zum Erstellen der Tabellen
    query = """
        CREATE TABLE IF NOT EXISTS user(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT
        )
    """
    
    query2 = """
        CREATE TABLE IF NOT EXISTS inventory(
            inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            quantity INTEGER,
            threshold INTEGER
        )
    """
    
    # Abfragen einzeln ausführen
    cur.execute(query)
    cur.execute(query2)
    
    print("Tabellen wurden erfolgreich erstellt.")

    # Abfrage, um die Tabellennamen anzuzeigen
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    # Tabellennamen anzeigen
    print("Tabellen in der Datenbank:")
    for table in tables:
        print(table[0])
    
    conn.close()

# Testbenutzer hinzufügen
def add_test_users():
    conn = sqlite3.connect("Database_Projekt_Bestandsliste.db")
    cur = conn.cursor()

    # Testbenutzer-Daten
    users = [
        ("admin", "adminpass", "Admin"),
        ("user1", "userpass1", "User"),
        ("user2", "userpass2", "User")
    ]

    for username, password, role in users:
        # Passwort hashen
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            # Benutzer hinzufügen
            cur.execute("INSERT INTO user (username, password_hash, role) VALUES (?, ?, ?)", (username, hashed_password, role))
            print(f"Benutzer {username} wurde hinzugefügt.")
        except sqlite3.IntegrityError:
            print(f"Benutzer {username} existiert bereits.")

    conn.commit()
    conn.close()

# Datenbank erstellen und Testbenutzer hinzufügen
create_database()
add_test_users()
