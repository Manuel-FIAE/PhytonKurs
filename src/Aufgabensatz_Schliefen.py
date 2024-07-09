# Benutzerdefinierte Eingabe für Start- und Endwert
start = int(input("Bitte geben Sie die Startzahl ein: "))
ende = int(input("Bitte geben Sie die Endzahl ein: "))


# Leere Liste zur Speicherung der geraden Zahlen
liste = []

# Schleife von Start bis Ende
for i in range(start, ende + 1):
    if i % 2 == 0:  # Überprüfung, ob die Zahl gerade ist
        liste.append(i)  # Hinzufügen der geraden Zahl zur Liste

liste.split("[]")
# Ausgabe der geraden Zahlen
print(f"Gerade Zahlen zwischen {start} und {ende}: {liste}")