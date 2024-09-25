import tkinter as tk

# Funktion zum Leeren der Eingabefelder
def clear_entries(entries):
    for entry in entries:
        entry.delete(0, tk.END)