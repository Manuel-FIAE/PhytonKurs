# SQL mit Python
import sqlite3  # Modul importieren

# Verbindung zur SQLite-Datenbank erstellen (oder erstellen, falls sie noch nicht existiert)
conn = sqlite3.connect("beispiel.db")  # Dateiendung sollte ".db" sein

# Cursor-Objekt erstellen
cur = conn.cursor()

# Tabelle erstellen, falls sie noch nicht existiert
#cur.execute("""
#                CREATE TABLE IF NOT EXISTS kunde(
#                    id INTEGER PRIMARY KEY,
#                    name TEXT NOT NULL,
#                    age INTEGER NOT NULL
#                )
#            """)

#Dateien einfügen
#cur.execute("""
#                INSERT INTO kunde (name,age)
#                VALUES ("Viktor",20),("Sascha",19)
#            """)
#cur.execute("""
#                INSERT INTO kunde (name,age)
#                VALUES ("Antonios",20)
#            """)

## Daten abfragen
#cur.execute(" SELECT * FROM kunde")
#rows = cur.fetchall()
#for row in rows:
#    print(row)
    
##Daten aktuekiesieren
#cur.execute("UPDATE kunde SET age = 40 WHERE name = 'Sascha'")

#Daten löschen 
#cur.execute("""
#            DELETE FROM kunde WHERE name = 'Sascha'
#            """)

# Änderung speichern (commit)
conn.commit()

# Verbindung schließen
conn.close()
