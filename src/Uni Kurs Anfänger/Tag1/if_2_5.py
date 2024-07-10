temepratur = input("Geben Sie an ob es warm oder kalt ist.\n Eingabe: ")
wetter = input("Geben Sie an ob es regenerisch, verschneit oder sonnig ist: \n Eingabe: ")
 
auswahl = temepratur+ " und " + wetter

print("Eingabe ", auswahl)

if(auswahl == "warm und regenerisch"):
    print("Ausgabe: Ein T-Shirt reicht nimm aber ein Regenschirm mit!")
elif(auswahl == "warm und verschneit"):
    print("Ausgabe: Nimm dir was warmes mit es schneit!")
elif(auswahl == "warm und sonnig"):
    print("Ausgabe: Ein T-Shirt reicht für heute völlig!")
elif(auswahl == " kalt und regenerisch"):
    print("Ausgabe: jcke und Regenschirm nicht vergessen")
elif(auswahl == "kalt und verschneit"):
    print("Ausgabe: Zieh dich sehr warm an!")
elif(auswahl == "kalt und sonnig"):
    print("Ausgabe: Zieh dir ein Jacke an und wenn es zu warm wird kannst du Sie ausziehen")
else:
    print("Falsche Eingabekalt")