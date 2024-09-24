import tkinter as tk
from tkinter import ttk

def convert_temperature():
    umwandlung = float(entry_value.get())
    selected_option = option_dropdown.current()  # Index der ausgewählten Option
    
    if selected_option == 0:
        result_label.config(text=f"Kelvin: {round(umwandlung + 273.15, 2)}")
    elif selected_option == 1:
        result_label.config(text=f"Fahrenheit: {round((umwandlung * (9/5)) + 32, 2)}")
    elif selected_option == 2:
        result_label.config(text=f"Celsius: {round(umwandlung - 273.15, 2)}")
    elif selected_option == 3:
        result_label.config(text=f"Fahrenheit: {round((umwandlung - 273.15) * (9/5) + 32, 2)}")
    elif selected_option == 4:
        result_label.config(text=f"Celsius: {round((umwandlung - 32) * (5/9), 2)}")
    elif selected_option == 5:
        result_label.config(text=f"Kelvin: {round((umwandlung - 32) * (5/9) + 273.15, 2)}")
    else:
        result_label.config(text="Falsche Eingabe")

def quit_program():
    root.destroy()

root = tk.Tk()
root.title("Temperaturumrechner")

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0)

# Input
ttk.Label(frame, text="Wert eingeben:").grid(row=0, column=0, sticky="w")
entry_value = ttk.Entry(frame, width=10)
entry_value.grid(row=0, column=1, padx=10)

# Dropdown für Optionen
ttk.Label(frame, text="Umrechnung auswählen:").grid(row=1, column=0, sticky="w")
option_dropdown = ttk.Combobox(frame, width=30, state="readonly")
option_dropdown['values'] = [
    "Umrechnung von Celsius nach Kelvin",
    "Umrechnung von Celsius nach Fahrenheit",
    "Umrechnung von Kelvin nach Celsius",
    "Umrechnung von Kelvin nach Fahrenheit",
    "Umrechnung von Fahrenheit nach Celsius",
    "Umrechnung von Fahrenheit nach Kelvin"
]
option_dropdown.grid(row=1, column=1, padx=10)
option_dropdown.current(0)

# Button für Umrechnung
convert_button = ttk.Button(frame, text="Umrechnen", command=convert_temperature)
convert_button.grid(row=2, column=0, columnspan=2, pady=10)

# Ausgabefeld für Ergebnisse
result_label = ttk.Label(frame, text="")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

# Button für Abbruch
quit_button = ttk.Button(frame, text="Programm beenden", command=quit_program)
quit_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
