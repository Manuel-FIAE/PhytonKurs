kon_number = int(input("Bitte geben Sie die zu konvertierende Zahl ein : "))
kon_change = int(input("Bite geben Sie die Basis ein(2 für Binär, 8 für Oktal, 16 für Hexadezimal): "))

list_answer = []

def Umwandler(kon_number, list_answer, kon_change):
    
    if(kon_change == 2):
        while(kon_number > 0):
            rest = kon_number % 2
            list_answer.append(rest)
            kon_number = kon_number // 2 
            
    if(kon_change == 8):
        while(kon_number > 0):
            rest = kon_number % 8
            list_answer.append(rest)
            kon_number = kon_number // 2 
    
    while(len(list_answer) < 4 ):     
        list_answer.append(0)      
        
    if(len(list_answer) > 4):
            while(len(list_answer) < 8 ):
                list_answer.append(0)   
                
    
        
    list_answer.reverse()
            

            
    print(f"Die Zahl {kon_number} in der Basis {kon_change} ist : {list_answer}")

#Umwandler(kon_number,list_answer,kon_change)

print(list_answer)

oki = 18 % 8
print(oki)