import math

def Options(option, umwandlung):
    if option == 1:
        print("Kelvin", round(umwandlung + 273.15, 2))
    elif option == 2:
        print("Fahrenheit", round((umwandlung * (9/5)) + 32, 2))
    elif option == 3:
        print("Celsius", round(umwandlung - 273.15, 2))
    elif option == 4:
        print("Fahrenheit", round((umwandlung - 273.15) * (9/5) + 32, 2))
    elif option == 5:
        print("Kelvin", round((umwandlung - 32) * (5/9), 2))
    elif option == 6:
        print("Kelvin", round((umwandlung - 32) * (5/9) + 273.15, 2))
    elif option == 7:
        return False
    else:
        print("Falsche Eingabe")
    return True

abbruch = True

while abbruch:
    umwandlung = float(input("Geben Sie den Wert ein, der umgewandelt werden soll: "))

    option = int(input("Welche Umwandlung wollen Sie machen?" 
                    "\n(1) Umrechnung von Celsius nach Kelvin" 
                    "\n(2) Umrechnung von Celsius nach Fahrenheit"
                    "\n(3) Umrechnung von Kelvin nach Celsius"
                    "\n(4) Umrechnung von Kelvin nach Fahrenheit"
                    "\n(5) Umrechnung von Fahrenheit nach Celsius"
                    "\n(6) Umrechnung von Fahrenheit nach Kelvin"
                    "\n(7) Abbruch des Programmes\nGeben Sie Ihre Wahl ein: "))

    abbruch = Options(option, umwandlung)
    
print("Programm zu Ende")
