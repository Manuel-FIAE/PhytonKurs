valueList = [20,50,70]

total = 0

if(valueList == []):
    print("Fehler")
else:
    for item in valueList:
        total += item
    
print(f"Der Wert ist {total}")