import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 
import logo

import tkinter as tk
from tkinter import messagebox
import sqlite3

import tkinter as tk
from tkinter import messagebox
import sqlite3

# Funktion zur Anzeige eines Rückmeldefensters (bereits implementiert)
def zeige_rueckmeldung(root, titel, nachricht, farbe, icon=None):
    popup = tk.Toplevel(root)
    popup.title(titel)
    popup.geometry("350x150")
    popup.configure(bg=farbe)
    popup.resizable(False, False)

    # Hintergrundfarbe des Fensters
    style_frame = tk.Frame(popup, bg=farbe)
    style_frame.pack(expand=True, fill="both")

    # Nachricht im Fenster anzeigen
    message_label = tk.Label(style_frame, text=nachricht, bg=farbe, fg="white", font=("Helvetica", 14, "bold"))
    message_label.pack(pady=10)

    # Fenster nach 2 Sekunden automatisch schließen
    popup.after(2000, popup.destroy)

# Funktion zur Bestätigungsabfrage mit allen Titeln
def frage_loeschen_bestätigung(root, buch_id_loeschen, titel_loeschen, autor_loeschen, genre_loeschen, jahr_loeschen):
    # Verbindung zur SQLite-Datenbank erstellen, um sicherzustellen, dass das Buch existiert
    conn = sqlite3.connect("C:\\Users\\Student\\Desktop\\Phytonkurs\\Phytonkurs\\src\\PhytonKurs\\src\\bücherverwaltung\\bücherverwaltung.db")
    cur = conn.cursor()

    # Abfrage nach allen passenden Büchern
    query = """
        SELECT titel FROM bücherverwaltung 
        WHERE buch_id = ? OR titel = ? OR autor = ? OR genre = ? OR year = ?
    """
    cur.execute(query, (buch_id_loeschen, titel_loeschen, autor_loeschen, genre_loeschen, jahr_loeschen))
    books = cur.fetchall()  # Alle übereinstimmenden Bücher abrufen

    # Verbindung schließen
    conn.close()

    if books:
        # Erstellen einer Liste mit allen gefundenen Titeln
        buch_titel_liste = "\n".join([f"- {book[0]}" for book in books])
        nachricht = f"Bist du sicher, dass du die folgenden Bücher löschen möchtest?\n\n{buch_titel_liste}"
        
        antwort = messagebox.askyesno("Löschen bestätigen", nachricht)
        
        if antwort:  # Wenn der Benutzer auf "Ja" klickt
            löschen_in_datenbank(root, buch_id_loeschen, titel_loeschen, autor_loeschen, genre_loeschen, jahr_loeschen)
        else:
            # Abbruch, falls der Benutzer auf "Nein" klickt
            zeige_rueckmeldung(root, "Abbruch", "Löschen wurde abgebrochen.", "orange")
    else:
        # Wenn kein Buch gefunden wurde
        zeige_rueckmeldung(root, "Fehler", "Es wurden keine Bücher gefunden, die gelöscht werden können.", "red")

# Löschen-Funktion mit Popup-Meldung bei Erfolg oder Fehler
def löschen_in_datenbank(root, buch_id_loeschen, titel_loeschen, autor_loeschen, genre_loeschen, jahr_loeschen):
    # Verbindung zur SQLite-Datenbank erstellen
    conn = sqlite3.connect("C:\\Users\\Student\\Desktop\\Phytonkurs\\Phytonkurs\\src\\PhytonKurs\\src\\bücherverwaltung\\bücherverwaltung.db")
    cur = conn.cursor()

    try:
        # Parameterbindung für Sicherheit und Vermeidung von SQL-Injection
        query = """
            DELETE FROM bücherverwaltung 
            WHERE buch_id = ? OR titel = ? OR autor = ? OR genre = ? OR year = ?
        """
        
        cur.execute(query, (buch_id_loeschen, titel_loeschen, autor_loeschen, genre_loeschen, jahr_loeschen))
        conn.commit()

        if cur.rowcount > 0:
            # Erfolgsmeldung anzeigen (grünes Fenster)            
            zeige_rueckmeldung(root, "Erfolg", "Bücher erfolgreich gelöscht!", "green")
        else:
            # Rückmeldung, wenn kein Buch gelöscht wurde
            zeige_rueckmeldung(root, "Fehler", "Die Bücher konnten nicht gelöscht werden, da sie nicht existieren.", "red")
    
    except Exception as e:
        # Fehler beim Löschen
        zeige_rueckmeldung(root, "Fehler", f"Fehler beim Löschen: {str(e)}", "red")

    # Verbindung schließen
    conn.close()
    
# Funktion für die dynamische Suchfunktion
def suche_in_datenbank(root, buch_id_suche, titel_suche, autor_suche, genre_suche, jahr_suche, gelesen_var):
    # Verbindung zur SQLite-Datenbank erstellen
    conn = sqlite3.connect("C:\\Users\\Student\\Desktop\\Phytonkurs\\Phytonkurs\\src\\PhytonKurs\\src\\bücherverwaltung\\bücherverwaltung.db")
    cur = conn.cursor()

    # Grundlegende SQL-Abfrage
    query = "SELECT * FROM bücherverwaltung WHERE 1=1"
    params = []

    # Dynamisches Hinzufügen von Kriterien
    if buch_id_suche:
        query += " AND buch_id = ?"
        params.append(buch_id_suche)
    
    if titel_suche:
        query += " AND titel LIKE ?"
        params.append(f"%{titel_suche}%")
    
    if autor_suche:
        query += " AND autor LIKE ?"
        params.append(f"%{autor_suche}%")
    
    if genre_suche:
        query += " AND genre LIKE ?"
        params.append(f"%{genre_suche}%")
    
    if jahr_suche:
        query += " AND year = ?"
        params.append(jahr_suche)
    
    # Lesestatus nur hinzufügen, wenn nicht "Beide" ausgewählt ist (gelesen_var != -1)
    if gelesen_var in [0, 1]:  # Nur wenn gelesen_var 0 (nicht gelesen) oder 1 (gelesen) ist
        query += " AND read = ?"
        params.append(gelesen_var)

    # Abfrage ausführen
    cur.execute(query, params)
    rows = cur.fetchall()

    # Neues Fenster für die Suchergebnisse
    data_window = tk.Toplevel(root)
    data_window.title("Suchergebnisse")
    data_window.geometry("950x400")
    
    # Setze das Logo im neuen Fenster (data_window)
    logo.set_window_logo(data_window, "C:\\Users\\Student\\Desktop\\Phytonkurs\\Phytonkurs\\src\\PhytonKurs\\src\\bücherverwaltung\\buchlabel.png")

    # Treeview für die Ergebnisse
    columns = ("Buch ID", "Titel", "Autor", "Genre", "Jahr", "Gelesen")
    tree = ttk.Treeview(data_window, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    # Spaltenüberschriften definieren
    tree.heading("Buch ID", text="Buch ID")
    tree.heading("Titel", text="Titel")
    tree.heading("Autor", text="Autor")
    tree.heading("Genre", text="Genre")
    tree.heading("Jahr", text="Jahr")
    tree.heading("Gelesen", text="Gelesen")

    # Spaltenbreiten anpassen
    tree.column("Buch ID", width=50)
    tree.column("Titel", width=200)
    tree.column("Autor", width=150)
    tree.column("Genre", width=100)
    tree.column("Jahr", width=50)
    tree.column("Gelesen", width=70)

    # Ergebnisse in die Tabelle einfügen
    for book in rows:
        tree.insert("", tk.END, values=(book[0], book[1], book[2], book[3], book[4], 'Ja' if book[5] == 1 else 'Nein'))

    # Verbindung schließen
    conn.close()



# Funktion für die dynamische Eingabe in die Datenbank
def eingabe_in_datenbank(root, titel_eingabe, autor_eingabe, genre_eingabe, jahr_eingabe, gelesen_var_eingabe):
    # Verbindung zur SQLite-Datenbank erstellen
    conn = sqlite3.connect("C:\\Users\\Student\\Desktop\\Phytonkurs\\Phytonkurs\\src\\PhytonKurs\\src\\bücherverwaltung\\bücherverwaltung.db")
    cur = conn.cursor()
    
    # Sicherstellen, dass keine leeren Felder eingegeben wurden
    if titel_eingabe and autor_eingabe and genre_eingabe and jahr_eingabe and gelesen_var_eingabe is not None:
        try:
            # Parameterbindung für Sicherheit und Vermeidung von SQL-Injection
            query = """
                INSERT INTO bücherverwaltung (titel, autor, genre, year, read)
                VALUES (?, ?, ?, ?, ?)
            """
            
            # Daten in die Datenbank einfügen
            cur.execute(query, (titel_eingabe, autor_eingabe, genre_eingabe, jahr_eingabe, gelesen_var_eingabe))
            
            # Änderungen speichern
            conn.commit()

            # Erfolgsmeldung anzeigen (grünes Fenster)
            zeige_rueckmeldung(root, "Erfolg", "Buch erfolgreich hinzugefügt!", "green")
        except Exception as e:
            # Fehler beim Einfügen
            zeige_rueckmeldung(root, "Fehler", f"Fehler beim Hinzufügen: {str(e)}", "red")
    else:
        # Bei nicht erfolgreichen Eingaben (rote Meldung)
        zeige_rueckmeldung(root, "Fehler", "Alle Felder müssen ausgefüllt sein!", "red")

    # Verbindung schließen
    conn.close()

from tkinter import messagebox

# Update-Funktion mit Popup-Meldung bei Erfolg oder Fehler
def update_in_datenbank(root, buch_id_update, titel_update, autor_update, genre_update, jahr_update, gelesen_var): 
    # Verbindung zur SQLite-Datenbank erstellen
    conn = sqlite3.connect("C:\\Users\\Student\\Desktop\\Phytonkurs\\Phytonkurs\\src\\PhytonKurs\\src\\bücherverwaltung\\bücherverwaltung.db")
    cur = conn.cursor()
    
    try:
        # Zuerst die Bücher anzeigen, die aktualisiert werden sollen
        query_select = """
            SELECT * FROM bücherverwaltung 
            WHERE buch_id = ? OR titel = ? OR autor = ? OR genre = ? OR year = ?
        """
        cur.execute(query_select, (buch_id_update, titel_update, autor_update, genre_update, jahr_update))
        rows = cur.fetchall()

        if not rows:
            # Falls keine Bücher gefunden wurden, Fehlermeldung anzeigen und Rückgabe
            zeige_rueckmeldung(root, "Fehler", "Keine Bücher gefunden, die aktualisiert werden können.", "red")
            conn.close()
            return

        # Zeige die gefundenen Bücher in einer Bestätigungsabfrage an
        buch_liste = "\n".join([f"ID: {row[0]}, Titel: {row[1]}, Autor: {row[2]}, Genre: {row[3]}, Jahr: {row[4]}, Gelesen: {'Ja' if row[5] == 1 else 'Nein'}" for row in rows])
        antwort = messagebox.askyesno("Bestätigung", f"Die folgenden Bücher werden aktualisiert:\n\n{buch_liste}\n\nMöchtest du fortfahren?")
        
        if antwort:  # Wenn der Benutzer auf "Ja" klickt, Update ausführen
            # Grundlegende SQL-Abfrage für das Update
            query_update = """
                UPDATE bücherverwaltung 
                SET read = ? 
                WHERE buch_id = ? OR titel = ? OR autor = ? OR genre = ? OR year = ?
            """
            cur.execute(query_update, (gelesen_var, buch_id_update, titel_update, autor_update, genre_update, jahr_update))
            conn.commit()

            # Erfolgsmeldung anzeigen (grünes Fenster)
            zeige_rueckmeldung(root, "Erfolg", "Buchstatus erfolgreich aktualisiert!", "green")
        else:
            # Wenn der Benutzer auf "Nein" klickt, das Update abbrechen
            zeige_rueckmeldung(root, "Abgebrochen", "Das Update wurde abgebrochen.", "orange")
    
    except Exception as e:
        # Fehler beim Aktualisieren
        zeige_rueckmeldung(root, "Fehler", f"Fehler beim Aktualisieren: {str(e)}", "red")
    
    # Verbindung schließen
    conn.close()
from tkinter import messagebox

# Update-Funktion mit Popup-Meldung bei Erfolg oder Fehler
def update_in_datenbank(root, buch_id_update, titel_update, autor_update, genre_update, jahr_update, gelesen_var): 
    # Verbindung zur SQLite-Datenbank erstellen
    conn = sqlite3.connect("C:\\Users\\Student\\Desktop\\Phytonkurs\\Phytonkurs\\src\\PhytonKurs\\src\\bücherverwaltung\\bücherverwaltung.db")
    cur = conn.cursor()
    
    try:
        # Zuerst die Bücher anzeigen, die aktualisiert werden sollen
        query_select = """
            SELECT * FROM bücherverwaltung 
            WHERE (buch_id = ? OR titel = ? OR autor = ? OR genre = ? OR year = ?)
        """
        cur.execute(query_select, (buch_id_update, titel_update, autor_update, genre_update, jahr_update))
        rows = cur.fetchall()

        if not rows:
            # Falls keine Bücher gefunden wurden, Fehlermeldung anzeigen und Rückgabe
            zeige_rueckmeldung(root, "Fehler", "Keine Bücher gefunden, die aktualisiert werden können.", "red")
            conn.close()
            return

        # Filter nur Bücher heraus, deren Lesestatus geändert werden muss
        zu_aktualisieren = [row for row in rows if row[5] != gelesen_var]

        if not zu_aktualisieren:
            # Falls keine Bücher einen veränderten Status benötigen
            zeige_rueckmeldung(root, "Information", "Der Lesestatus dieser Bücher ist bereits korrekt.", "orange")
            conn.close()
            return

        # Zeige die Bücher, deren Status geändert wird
        buch_liste = "\n".join([f"ID: {row[0]}, Titel: {row[1]}, Autor: {row[2]}, Genre: {row[3]}, Jahr: {row[4]}, Gelesen: {'Ja' if row[5] == 1 else 'Nein'}" for row in zu_aktualisieren])
        antwort = messagebox.askyesno("Bestätigung", f"Die folgenden Bücher werden aktualisiert:\n\n{buch_liste}\n\nMöchtest du fortfahren?")
        
        if antwort:  # Wenn der Benutzer auf "Ja" klickt, Update ausführen
            # Grundlegende SQL-Abfrage für das Update
            query_update = """
                UPDATE bücherverwaltung 
                SET read = ? 
                WHERE buch_id = ? OR titel = ? OR autor = ? OR genre = ? OR year = ?
            """
            for row in zu_aktualisieren:
                cur.execute(query_update, (gelesen_var, row[0], row[1], row[2], row[3], row[4]))

            conn.commit()

            # Erfolgsmeldung anzeigen (grünes Fenster)
            zeige_rueckmeldung(root, "Erfolg", "Buchstatus erfolgreich aktualisiert!", "green")
        else:
            # Wenn der Benutzer auf "Nein" klickt, das Update abbrechen
            zeige_rueckmeldung(root, "Abgebrochen", "Das Update wurde abgebrochen.", "orange")
    
    except Exception as e:
        # Fehler beim Aktualisieren
        zeige_rueckmeldung(root, "Fehler", f"Fehler beim Aktualisieren: {str(e)}", "red")
    
    # Verbindung schließen
    conn.close()


# Funktion für die dynamische Suchfunktion
def suche_in_datenbank(root, buch_id_suche,titel_suche, autor_suche, genre_suche, jahr_suche, gelesen_var):
    # Verbindung zur SQLite-Datenbank erstellen
    conn = sqlite3.connect("C:\\Users\\Student\\Desktop\\Phytonkurs\\Phytonkurs\\src\\PhytonKurs\\src\\bücherverwaltung\\bücherverwaltung.db")
    cur = conn.cursor()

    # Grundlegende SQL-Abfrage
    query = "SELECT * FROM bücherverwaltung WHERE 1=1"
    params = []

    # Dynamisches Hinzufügen von Kriterien
    if buch_id_suche:
        query += " AND buch_id = ?"
        params.append(buch_id_suche)
    
    if titel_suche:
        query += " AND titel LIKE ?"
        params.append(f"%{titel_suche}%")
    
    if autor_suche:
        query += " AND autor LIKE ?"
        params.append(f"%{autor_suche}%")
    
    if genre_suche:
        query += " AND genre LIKE ?"
        params.append(f"%{genre_suche}%")
    
    if jahr_suche:
        query += " AND year = ?"
        params.append(jahr_suche)
    
    # Lesestatus hinzufügen, wenn eine Auswahl getroffen wurde
    if gelesen_var != -1:  # Wenn gelesen_var -1 ist, wurde nichts ausgewählt
        query += " AND read = ?"
        params.append(gelesen_var)

    # Abfrage ausführen
    cur.execute(query, params)
    rows = cur.fetchall()

    # Neues Fenster für die Suchergebnisse
    data_window = tk.Toplevel(root)
    data_window.title("Suchergebnisse")
    data_window.geometry("950x400")
    
    # Setze das Logo im neuen Fenster (data_window)
    logo.set_window_logo(data_window, "C:\\Users\\Student\\Desktop\\Phytonkurs\\Phytonkurs\\src\\PhytonKurs\\src\\bücherverwaltung\\buchlabel.png")

    # Treeview für die Ergebnisse
    columns = ("Buch ID", "Titel", "Autor", "Genre", "Jahr", "Gelesen")
    tree = ttk.Treeview(data_window, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    # Spaltenüberschriften definieren
    tree.heading("Buch ID", text="Buch ID")
    tree.heading("Titel", text="Titel")
    tree.heading("Autor", text="Autor")
    tree.heading("Genre", text="Genre")
    tree.heading("Jahr", text="Jahr")
    tree.heading("Gelesen", text="Gelesen")

    # Spaltenbreiten anpassen
    tree.column("Buch ID", width=50)
    tree.column("Titel", width=200)
    tree.column("Autor", width=150)
    tree.column("Genre", width=100)
    tree.column("Jahr", width=50)
    tree.column("Gelesen", width=70)

    # Ergebnisse in die Tabelle einfügen
    for book in rows:
        tree.insert("", tk.END, values=(book[0], book[1], book[2], book[3], book[4], 'Ja' if book[5] == 1 else 'Nein'))

    # Verbindung schließen
    conn.close()

# Gesamt-Ausgabe-Funktion (falls sie auch benötigt wird)
def gesamtAusgabe(root):
    conn = sqlite3.connect("C:\\Users\\Student\\Desktop\\Phytonkurs\\Phytonkurs\\src\\PhytonKurs\\src\\bücherverwaltung\\bücherverwaltung.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM bücherverwaltung")
    rows = cur.fetchall()
    
    data_window = tk.Toplevel(root)
    data_window.title("Liste der Bücher")
    data_window.geometry("950x400")
    
    # Setze das Logo im neuen Fenster (data_window)
    logo.set_window_logo(data_window, "C:\\Users\\Student\\Desktop\\Phytonkurs\\Phytonkurs\\src\\PhytonKurs\\src\\bücherverwaltung\\buchlabel.png")

    columns = ("Buch ID", "Titel", "Autor", "Genre", "Jahr", "Gelesen")
    tree = ttk.Treeview(data_window, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    tree.heading("Buch ID", text="Buch ID")
    tree.heading("Titel", text="Titel")
    tree.heading("Autor", text="Autor")
    tree.heading("Genre", text="Genre")
    tree.heading("Jahr", text="Jahr")
    tree.heading("Gelesen", text="Gelesen")

    tree.column("Buch ID", width=50)
    tree.column("Titel", width=200)
    tree.column("Autor", width=150)
    tree.column("Genre", width=100)
    tree.column("Jahr", width=50)
    tree.column("Gelesen", width=70)

    for book in rows:
        tree.insert("", tk.END, values=(book[0], book[1], book[2], book[3], book[4], 'Ja' if book[5] == 1 else 'Nein'))

    conn.close()
