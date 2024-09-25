import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqllie as db  # Dein Modul 'sqllie' importieren
import logo
import entry_delete as ed

# Hauptfenster erstellen
root = tk.Tk()
root.title("Bücherverwaltung")
root.geometry("950x700")

logo.set_window_logo(root, "C:/Users/Student/Desktop/Phytonkurs/Phytonkurs/src/PhytonKurs/src/bücherverwaltung/buchlabel.png")

# Canvas für den Scrollbereich erstellen
canvas = tk.Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

# Scrollbars erstellen (horizontal und vertikal)
scrollbar_y = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar_y.pack(side="right", fill="y")

scrollbar_x = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
scrollbar_x.pack(side="bottom", fill="x")

# Frame in der Canvas erstellen, der gescrollt werden kann
scrollable_frame = tk.Frame(canvas)

# Fenster in der Canvas erstellen, in das der Frame eingefügt wird
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Scroll-Funktionalität hinzufügen
def configure_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_scrollregion)

# Scrollbars mit der Canvas verknüpfen
canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

# Frame für Logo und Titel erstellen
top_frame = tk.Frame(scrollable_frame)
top_frame.pack(pady=10, padx=20, anchor="w")

# Logo hinzufügen (vorausgesetzt, du hast Pillow installiert und ein Bild im selben Verzeichnis)
logo_image = Image.open("C:/Users/Student/Desktop/Phytonkurs/Phytonkurs/src/PhytonKurs/src/bücherverwaltung/buchlabel.png")
logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
logo = ImageTk.PhotoImage(logo_image)

# Label für das Logo hinzufügen
logo_label = tk.Label(top_frame, image=logo)
logo_label.pack(side="left", padx=10)

# Überschrift neben dem Logo hinzufügen
headline = tk.Label(top_frame, text="Bücherverwaltung", font=("Helvetica", 24, "bold underline"))
headline.pack(side="left", padx=10)

# Gesamten Fensterbereich in einem LabelFrame für eine Umrandung
main_frame = tk.LabelFrame(scrollable_frame, text="Bücherverwaltung", font=("Helvetica", 12, "bold"), padx=10, pady=10)
main_frame.pack(fill="both", expand="yes", padx=20, pady=20)

# 1. Frame für "Buch hinzufügen" mit Umrandung
frame_hinzufuegen = tk.LabelFrame(main_frame, text="Buch hinzufügen", font=("Helvetica", 12, "bold"), padx=10, pady=10)
frame_hinzufuegen.pack(fill="both", expand="yes", padx=10, pady=10)

# Labels und Eingabefelder für Buch hinzufügen
tk.Label(frame_hinzufuegen, text="Titel:").grid(row=0, column=0, padx=5, pady=5)
titel = tk.Entry(frame_hinzufuegen)
titel.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_hinzufuegen, text="Autor:").grid(row=0, column=2, padx=5, pady=5)
autor = tk.Entry(frame_hinzufuegen)
autor.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_hinzufuegen, text="Genre:").grid(row=0, column=4, padx=5, pady=5)
genre = tk.Entry(frame_hinzufuegen)
genre.grid(row=0, column=5, padx=5, pady=5)

tk.Label(frame_hinzufuegen, text="Jahr:").grid(row=0, column=6, padx=5, pady=5)
jahr = tk.Entry(frame_hinzufuegen)
jahr.grid(row=0, column=7, padx=5, pady=5)

# Radiobuttons für Lesestatus innerhalb des "Buch hinzufügen"-Bereichs
lesestatus_var = tk.IntVar()
gelesen_button = tk.Radiobutton(frame_hinzufuegen, text="Gelesen", variable=lesestatus_var, value=1)
gelesen_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")

nicht_gelesen_button = tk.Radiobutton(frame_hinzufuegen, text="Nicht gelesen", variable=lesestatus_var, value=0)
nicht_gelesen_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Button zum Bestätigen (Daten in Datenbank speichern)
button_buch_hinzufuegen = tk.Button(frame_hinzufuegen, text="Hinzufügen", command=lambda: db.eingabe_in_datenbank(
    root, 
    titel.get(),  # Verwende das Entry-Feld für Titel
    autor.get(),  # Verwende das Entry-Feld für Autor
    genre.get(),  # Verwende das Entry-Feld für Genre
    jahr.get(),   # Verwende das Entry-Feld für Jahr
    lesestatus_var.get()  
))
button_buch_hinzufuegen.grid(row=3, column=0, columnspan=8, pady=10, sticky="w")

clear_button = tk.Button(frame_hinzufuegen, text="Eingaben leeren", command=lambda: ed.clear_entries([titel, autor, genre, jahr]))
clear_button.grid(row=3, column=1, columnspan=4, pady=10, sticky="w")

# 2. Frame für die Suchfunktion mit Umrandung
frame_suchfunktion = tk.LabelFrame(main_frame, text="Suchfunktion", font=("Helvetica", 12, "bold"), padx=10, pady=10)
frame_suchfunktion.pack(fill="both", expand="yes", padx=10, pady=10)

# Neues Frame speziell für das grid() Layout innerhalb der Suchfunktion
grid_frame_suchfunktion = tk.Frame(frame_suchfunktion)
grid_frame_suchfunktion.pack()

# Labels und Eingabefelder für die Suchfunktion nebeneinander anordnen (grid verwenden)
tk.Label(grid_frame_suchfunktion, text="Titel:").grid(row=0, column=0, padx=5, pady=5)
titel_suche = tk.Entry(grid_frame_suchfunktion)
titel_suche.grid(row=0, column=1, padx=5, pady=5)

tk.Label(grid_frame_suchfunktion, text="Autor:").grid(row=0, column=2, padx=5, pady=5)
autor_suche = tk.Entry(grid_frame_suchfunktion)
autor_suche.grid(row=0, column=3, padx=5, pady=5)

tk.Label(grid_frame_suchfunktion, text="Genre:").grid(row=0, column=4, padx=5, pady=5)
genre_suche = tk.Entry(grid_frame_suchfunktion)
genre_suche.grid(row=0, column=5, padx=5, pady=5)

tk.Label(grid_frame_suchfunktion, text="Jahr:").grid(row=0, column=6, padx=5, pady=5)
jahr_suche = tk.Entry(grid_frame_suchfunktion)
jahr_suche.grid(row=0, column=7, padx=5, pady=5)

lesestatus_suche_var = tk.IntVar()
gelesen_button_suche = tk.Radiobutton(grid_frame_suchfunktion, text="Gelesen", variable=lesestatus_suche_var, value=1)
gelesen_button_suche.grid(row=2, column=0, padx=5, pady=5, sticky="w")
nicht_gelesen_button_suche = tk.Radiobutton(grid_frame_suchfunktion, text="Nicht gelesen", variable=lesestatus_suche_var, value=0)
nicht_gelesen_button_suche.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Button für die Suchfunktion
button_suchfunktion = tk.Button(grid_frame_suchfunktion, text="Suchfunktion", command=lambda: db.suche_in_datenbank(
    root, 
    titel_suche.get(), 
    autor_suche.get(), 
    genre_suche.get(), 
    jahr_suche.get(), 
    lesestatus_suche_var.get() if lesestatus_suche_var.get() in [0, 1] else None
))
button_suchfunktion.grid(row=3, column=0, columnspan=8, pady=10, sticky="w")

# Button zum Leeren der Eingabefelder
clear_button = tk.Button(grid_frame_suchfunktion, text="Eingaben leeren", command=lambda: ed.clear_entries([titel_suche, autor_suche, genre_suche, jahr_suche]))
clear_button.grid(row=3, column=1, columnspan=4, pady=10, padx=8, sticky="w")

# 3. Frame für "Liste der Bücher ausgeben" mit Umrandung
frame_liste = tk.LabelFrame(main_frame, text="Liste der Bücher", font=("Helvetica", 12, "bold"), padx=10, pady=10)
frame_liste.pack(fill="both", expand="yes", padx=10, pady=10)

# Label für "Liste der Bücher ausgeben"
listebuecher = tk.Label(frame_liste, text="Liste der Bücher ausgeben", font=("Helvetica", 11))
listebuecher.pack(anchor="w", pady=5)

# Button für die Listenanzeige linksbündig
button_liste = tk.Button(frame_liste, text="Listen Auswahl", command=lambda: db.gesamtAusgabe(root))
button_liste.pack(anchor="w", pady=5, padx=5)

# 4. Frame für "Buch löschen" mit Umrandung
frame_loeschen = tk.LabelFrame(main_frame, text="Buch löschen", font=("Helvetica", 12, "bold"), padx=10, pady=10)
frame_loeschen.pack(fill="both", expand="yes", padx=10, pady=10)

# Labels und Eingabefelder für Buch löschen
tk.Label(frame_loeschen, text="Titel:").grid(row=0, column=0, padx=5, pady=5)
titel_loeschen = tk.Entry(frame_loeschen)
titel_loeschen.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_loeschen, text="Autor:").grid(row=0, column=2, padx=5, pady=5)
autor_loeschen = tk.Entry(frame_loeschen)
autor_loeschen.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_loeschen, text="Genre:").grid(row=0, column=4, padx=5, pady=5)
genre_loeschen = tk.Entry(frame_loeschen)
genre_loeschen.grid(row=0, column=5, padx=5, pady=5)

tk.Label(frame_loeschen, text="Jahr:").grid(row=0, column=6, padx=5, pady=5)
jahr_loeschen = tk.Entry(frame_loeschen)
jahr_loeschen.grid(row=0, column=7, padx=5, pady=5)

# Button zum Bestätigen (Daten in Datenbank löschen)
button_buch_loeschen = tk.Button(frame_loeschen, text="Löschen", command=lambda: db.löschen_in_datenbank(
    root, 
    titel_loeschen.get(),  # Verwende das Entry-Feld für Titel
    autor_loeschen.get(),  # Verwende das Entry-Feld für Autor
    genre_loeschen.get(),  # Verwende das Entry-Feld für Genre
    jahr_loeschen.get(),   # Verwende das Entry-Feld für Jahr
))
button_buch_loeschen.grid(row=3, column=0, columnspan=8, pady=10, sticky="w")

# Button zum Leeren der Eingabefelder
clear_button = tk.Button(frame_loeschen, text="Eingaben leeren", command=lambda: ed.clear_entries([titel_loeschen, autor_loeschen, genre_loeschen, jahr_loeschen]))
clear_button.grid(row=3, column=1, columnspan=4, pady=10, padx=18, sticky="w")

# Hauptschleife
root.mainloop()
