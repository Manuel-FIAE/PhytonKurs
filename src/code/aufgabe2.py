counter = True;

number = 1000.05

while(counter):
    if((number / 2) > 1):
        print(f"Noch über 1")
        print(number)
        number /= 2
    else:
        print(f"Nicht mehr über 1")        
        print(number / 2)
        counter = False
