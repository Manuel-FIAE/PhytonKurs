import tkinter as tk
from tkinter import ttk
import sqlite3 
import logo


# Funktion zur Anzeige eines Rückmeldefensters
def zeige_rueckmeldung(root, titel, nachricht, farbe, icon=None):
    # Neues TopLevel-Fenster erstellen
    popup = tk.Toplevel(root)
    popup.title(titel)

    # Größe des Fensters einstellen und Stil verbessern
    popup.geometry("350x150")
    popup.configure(bg=farbe)
    popup.resizable(False, False)

    # Hintergrundfarbe des Fensters
    style_frame = tk.Frame(popup, bg=farbe)
    style_frame.pack(expand=True, fill="both")

    # Optional: Icon hinzufügen
    if icon:
        icon_label = tk.Label(style_frame, image=icon, bg=farbe)
        icon_label.pack(pady=10)

    # Nachricht im Fenster anzeigen (zentriert mit größerer Schriftart)
    message_label = tk.Label(style_frame, text=nachricht, bg=farbe, fg="white", font=("Helvetica", 14, "bold"))
    message_label.pack(pady=10)

    # Button "OK", um das Fenster manuell zu schließen
    ok_button = tk.Button(style_frame, text="OK", command=popup.destroy, font=("Helvetica", 10), relief="flat", bg="white", fg=farbe)
    ok_button.pack(pady=5)

    # Fenster nach 3 Sekunden automatisch schließen, falls OK nicht gedrückt wird
    popup.after(3000, popup.destroy)
    
def update_in_datenbank(root, titel_loeschen, autor_loeschen, genre_loeschen, jahr_loeschen): 
    print("ok ")

def löschen_in_datenbank(root, titel_loeschen, autor_loeschen, genre_loeschen, jahr_loeschen):
    # Verbindung zur SQLite-Datenbank erstellen
    conn = sqlite3.connect("bücherverwaltung.db")
    cur = conn.cursor()

    try:
        # Parameterbindung für Sicherheit und Vermeidung von SQL-Injection
        query = """
            DELETE FROM bücherverwaltung 
            WHERE titel = ? OR autor = ? OR genre = ? OR year = ?
        """
        
        # Daten in die Datenbank einfügen
        cur.execute(query, (titel_loeschen , autor_loeschen , genre_loeschen , jahr_loeschen ))
                    # Änderungen speichern
        conn.commit()

        # Erfolgsmeldung anzeigen (grünes Fenster)            
        zeige_rueckmeldung(root, "Erfolg", "Buch erfolgreich gelöscht!", "green")
    except Exception as e:
        # Fehler beim Einfügen
        zeige_rueckmeldung(root, "Fehler", f"Fehler beim löschen: {str(e)}", "red")

    # Verbindung schließen
    conn.close()

# Funktion für die dynamische Eingabe in die Datenbank
def eingabe_in_datenbank(root, titel_eingabe, autor_eingabe, genre_eingabe, jahr_eingabe, gelesen_var_eingabe):
    # Verbindung zur SQLite-Datenbank erstellen
    conn = sqlite3.connect("bücherverwaltung.db")
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


# Funktion für die dynamische Suchfunktion
def suche_in_datenbank(root, titel_suche, autor_suche, genre_suche, jahr_suche, gelesen_var):
    # Verbindung zur SQLite-Datenbank erstellen
    conn = sqlite3.connect("bücherverwaltung.db")
    cur = conn.cursor()

    # Grundlegende SQL-Abfrage
    query = "SELECT * FROM bücherverwaltung WHERE 1=1"
    params = []

    # Dynamisches Hinzufügen von Kriterien
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
    logo.set_window_logo(data_window, "C:/Users/Student/Desktop/Phytonkurs/Phytonkurs/src/PhytonKurs/src/bücherverwaltung/buchlabel.png")

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
    conn = sqlite3.connect("bücherverwaltung.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM bücherverwaltung")
    rows = cur.fetchall()
    
    data_window = tk.Toplevel(root)
    data_window.title("Liste der Bücher")
    data_window.geometry("950x400")
    
    # Setze das Logo im neuen Fenster (data_window)
    logo.set_window_logo(data_window, "C:/Users/Student/Desktop/Phytonkurs/Phytonkurs/src/PhytonKurs/src/bücherverwaltung/buchlabel.png")

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
