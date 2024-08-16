import tkinter as tk
from tkinter import messagebox, ttk

def berechne_annuitaet():
    try:
        if var_berechnung.get() == 1:  # Berechnung auf Basis des Kaufpreises
            kaufpreis = float(entry_kaufpreis.get())
            eigenkapital = float(entry_eigenkapital.get())
            zinssatz = float(entry_zinssatz.get()) / 100 / 12  # Zinssatz pro Monat
            tilgung = float(entry_tilgung.get()) / 100  # Anfangstilgung (pro Jahr)
            darlehensbetrag = kaufpreis - eigenkapital

            # Berechne die monatliche Annuität
            annuitaet = round(darlehensbetrag * (zinssatz + tilgung / 12), 2)
        elif var_berechnung.get() == 2:  # Berechnung auf Basis der monatlichen Rate
            monatliche_rate = float(entry_monatsrate.get())
            zinssatz = float(entry_zinssatz.get()) / 100 / 12  # Zinssatz pro Monat
            tilgung = float(entry_tilgung.get()) / 100  # Anfangstilgung (pro Jahr)

            # Berechne den Darlehensbetrag basierend auf der Rate
            darlehensbetrag = round(monatliche_rate / (zinssatz + tilgung / 12), 2)
            eigenkapital = float(entry_eigenkapital.get())
            kaufpreis = round(darlehensbetrag + eigenkapital, 2)
            label_kaufpreis.config(text=f"Kaufpreis: {kaufpreis:.2f} €")
            
            # Die Annuität ist die gegebene monatliche Rate
            annuitaet = monatliche_rate

        # Berechnung der Tilgungstabelle
        restschuld = darlehensbetrag
        monate = 0
        jahr = 1
        daten = []

        while restschuld > 0:
            zinsen = round(restschuld * zinssatz, 2)
            tilgungsanteil = round(annuitaet - zinsen, 2)
            restschuld = round(restschuld - tilgungsanteil, 2)
            monate += 1

            if restschuld < 0:
                restschuld = 0

            if monate % 12 == 1:  # Neues Jahr beginnt
                daten.append((f"Jahr {jahr}", "", "", "", ""))
                jahr += 1

            daten.append((monate, annuitaet, zinsen, tilgungsanteil, restschuld))

        zeige_tabelle(daten)

    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige Zahlen ein.")

def zeige_tabelle(daten):
    # Neues Fenster für die Tabelle erstellen
    tabelle_fenster = tk.Toplevel(root)
    tabelle_fenster.title("Tilgungstabelle")

    # Scrollbar hinzufügen
    scrollbar = tk.Scrollbar(tabelle_fenster)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Tabelle erstellen
    columns = ('Monat', 'Rate', 'Zinsen', 'Tilgung', 'Restschuld')
    tree = ttk.Treeview(tabelle_fenster, columns=columns, show='headings', yscrollcommand=scrollbar.set)

    # Spaltenüberschriften
    for col in columns:
        tree.heading(col, text=col)

    # Daten einfügen
    for row in daten:
        tree.insert("", tk.END, values=row)

    tree.pack(fill=tk.BOTH, expand=True)

    # Scrollbar mit der Tabelle verbinden
    scrollbar.config(command=tree.yview)

def update_entry_fields():
    if var_berechnung.get() == 1:
        entry_kaufpreis.config(state=tk.NORMAL, bg="white")
        entry_monatsrate.config(state=tk.DISABLED, bg="lightgrey")
    elif var_berechnung.get() == 2:
        entry_kaufpreis.config(state=tk.DISABLED, bg="lightgrey")
        entry_monatsrate.config(state=tk.NORMAL, bg="white")

# Hauptfenster erstellen
root = tk.Tk()
root.title("Annuitätenrechner")

# Labels und Eingabefelder
tk.Label(root, text="Eigenkapital (€):").grid(row=0, column=0, padx=10, pady=10)
entry_eigenkapital = tk.Entry(root)
entry_eigenkapital.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Zinssatz (%):").grid(row=1, column=0, padx=10, pady=10)
entry_zinssatz = tk.Entry(root)
entry_zinssatz.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Anfangstilgung (%):").grid(row=2, column=0, padx=10, pady=10)
entry_tilgung = tk.Entry(root)
entry_tilgung.grid(row=2, column=1, padx=10, pady=10)

# Eingabefelder für Kaufpreis oder Monatsrate
tk.Label(root, text="Kaufpreis (€):").grid(row=3, column=0, padx=10, pady=10)
entry_kaufpreis = tk.Entry(root)
entry_kaufpreis.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Monatsrate (€):").grid(row=4, column=0, padx=10, pady=10)
entry_monatsrate = tk.Entry(root, state=tk.DISABLED, bg="lightgrey")
entry_monatsrate.grid(row=4, column=1, padx=10, pady=10)

# Berechnungsbutton
button_berechnen = tk.Button(root, text="Berechnen", command=berechne_annuitaet)
button_berechnen.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Ergebnislabel
label_kaufpreis = tk.Label(root, text="")
label_kaufpreis.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Wahl zwischen Kaufpreis und Monatsrate
var_berechnung = tk.IntVar(value=1)
radiobutton_kaufpreis = tk.Radiobutton(root, text="Berechnung auf Basis des Kaufpreises", variable=var_berechnung, value=1, command=update_entry_fields)
radiobutton_kaufpreis.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

radiobutton_monatsrate = tk.Radiobutton(root, text="Berechnung auf Basis der Monatsrate", variable=var_berechnung, value=2, command=update_entry_fields)
radiobutton_monatsrate.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Hauptschleife starten
root.mainloop()
