zahl1 = 25
zahl2 = 40
zahl3 = 15

print(f"Ursprüngliche Zahlen: Zahl1 = {zahl1}, Zahl2 = {zahl2}, Zahl3 = {zahl3}")

zahlenliste = []

# Sortierung nach deinem Ansatz
if zahl1 <= zahl2 <= zahl3:
    zahlenliste = [zahl1, zahl2, zahl3]
elif zahl1 <= zahl3 <= zahl2:
    zahlenliste = [zahl1, zahl3, zahl2]
elif zahl2 <= zahl1 <= zahl3:
    zahlenliste = [zahl2, zahl1, zahl3]
elif zahl2 <= zahl3 <= zahl1:
    zahlenliste = [zahl2, zahl3, zahl1]
elif zahl3 <= zahl1 <= zahl2:
    zahlenliste = [zahl3, zahl1, zahl2]
elif zahl3 <= zahl2 <= zahl1:
    zahlenliste = [zahl3, zahl2, zahl1]

print("Sortierte Zahlen:", zahlenliste)
