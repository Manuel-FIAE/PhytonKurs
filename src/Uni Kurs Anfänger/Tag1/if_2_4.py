# 2.4 Uberprufe, ob ein vorher festgelegtes Jahr ein Schaltjahr ist. Dabei sind folgende Regeln zu beachten:

jahrezahl = int(input("Gib ne Jahreszahl ein: "))

if(jahrezahl % 4 == 0):
    if(jahrezahl % 100 == 0):
        if(jahrezahl % 400 == 0):
            print("Schaltjahr")
        else:
            print("KeinSchaltjahr")
    else:
        print("Schaltjahr")
else:
    print("Kein Schaltjahr")