# SQL mit Python
import sqlite3  # Modul importieren

# Verbindung zur SQLite-Datenbank erstellen (oder erstellen, falls sie noch nicht existiert)
conn = sqlite3.connect("bücherverwaltung.db")  # Dateiendung sollte ".db" sein

# Cursor-Objekt erstellen
cur = conn.cursor()

# Tabelle erstellen, falls sie noch nicht existiert
cur.execute("""
                CREATE TABLE IF NOT EXISTS bücherverwaltung(
                    buch_id INTEGER PRIMARY KEY,
                    titel TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    genere TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    read BOOLEAN NOT NULL
                )
            """)

# Änderung speichern (commit)
conn.commit()

# Verbindung schließen
conn.close()
