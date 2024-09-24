import tkinter as tk # Modul importieren als tk

def start():
    name = eingabe1.get() # Eingabefeld inhalt speichern 
    label3.config(text="Hallo " + name)

# Hauptfenster
root = tk.Tk()
root.title("Mein erstes Programm")
root.geometry("500x200")

label1 = tk.Label(root, text = "Willkommen zu meinem Programm")
label1.pack(pady=10)
#label1.place(x=0,y=0)

label2 = tk.Label(root, text = "Bitte, Name eingeben")
label2.pack(pady=5)

label3 = tk.Label(root)
label3.pack()

eingabe1 = tk.Entry(root)
eingabe1.pack(pady=5)

button1 = tk.Button(root, text = "Start", command = start)
button1.pack(pady=10)

# Hauptschleife 
root.mainloop()