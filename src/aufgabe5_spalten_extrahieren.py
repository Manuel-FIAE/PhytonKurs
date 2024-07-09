data = "1,2,3"

# Split den String an den Kommata
values = data.split(",")

# Gebe die Werte zeilenweise aus
for index in range(len(values)):
    print(f"{values[index]}")