def istGerade(zahl):
    return zahl % 2 == 0

valueList = [50,60,70,53,97,98,87,51,49,99,100]

for index in range(len(valueList)):
    if istGerade(valueList[index]):
        print(f"Die Zahl {valueList[index]} ist gerade    : Rückgabewert als Bestätigung {istGerade(valueList[index])}")
    else:
        print(f"Die Zahl {valueList[index]} ist ungerade  : Rückgabewert als Bestätigung {istGerade(valueList[index])}")    