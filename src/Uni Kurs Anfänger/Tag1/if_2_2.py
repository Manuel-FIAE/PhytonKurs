# Bestimme die Groesste aus drei vorher festgelegten Zahlen und gib diese Zahl aus.

zahl1 = 25
zahl2 = 10
zahl3 = 15

print(f"Zahl 1 : {zahl1} und Zahl 2: {zahl2} und Zahl3: {zahl3}")

if((zahl1 > zahl2) and (zahl1 > zahl3)):
    print("Die größere Zahl ist",zahl1)
else:
    if zahl2 > zahl3:
        print("Die größere Zahl ist",zahl2)
    else:
        print("Die größere Zahl ist",zahl3)