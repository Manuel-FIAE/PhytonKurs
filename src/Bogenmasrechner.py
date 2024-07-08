import math

# Benutzerinput für den Winkel im Bogenmaß
winkelbogenmass = float(input("Bitte geben Sie einen Winkel im Bogenmaß ein: "))

# Umrechnung von Bogenmaß in Grad
winkelgrad = winkelbogenmass * (180 / math.pi)
print("Grad:", winkelgrad)

# Grad in den ganzzahligen Teil und den Dezimalteil aufteilen
grad_ganz = int(winkelgrad)
grad_dezimal = winkelgrad - grad_ganz

# Umrechnung des Dezimalteils der Grad in Bogenminuten
winkelminuten_total = grad_dezimal * 60
minuten_ganz = int(winkelminuten_total)
minuten_dezimal = winkelminuten_total - minuten_ganz

print("Grad (ganz):", grad_ganz)
print("Grad (dezimal):", grad_dezimal)
print("Bogenminuten (gesamt):", winkelminuten_total)
print("Bogenminuten (ganz):", minuten_ganz)
print("Bogenminuten (dezimal):", minuten_dezimal)

# Umrechnung des Dezimalteils der Bogenminuten in Bogensekunden
bogensekunden = minuten_dezimal * 60

# Ergebnisse anzeigen
print("Grad:", grad_ganz)
print("Bogenminuten:", minuten_ganz)
print("Bogensekunden:", bogensekunden)
