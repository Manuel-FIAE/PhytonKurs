def fizzbuzz():
    
    # Eingaben für Start- und Endzahl
    num = int(input("Gebe Startzahl an: "))
    count = int(input("Gebe die Endzahl an: "))
    
        # Sicherstellen, dass die Startzahl kleiner oder gleich der Endzahl ist
    if num > count:
        print("Die Startzahl muss kleiner oder gleich der Endzahl sein.")
        return
    
    # FizzBuzz-Logik
    for num in range(num,count+1):
        if((num%3 == 0) and (num%5 == 0)):
            print("FizzBuzz")
        elif(num%3 == 0  ):
            print("Fizz")
        elif(num%5 == 0):
            print("Buzz")
        elif(num%7 == 0):
            print("Bazz")        
        else:
            print(num)
        
fizzbuzz()
    