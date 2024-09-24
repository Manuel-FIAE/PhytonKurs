def word_count():
    satzzeichen = [',', '.', '!', '?', ':', ';', '-', '(', ')', '"', "'"]

    # Benutzereingabe
    sentence = input("Geben Sie einen Satz ein: \n").lower()
    
    # Entfernen der Satzzeichen
    sentence = "".join(char for char in sentence if char not in satzzeichen)
    
    # Text in Wörter aufteilen
    words = sentence.split()
    
    # Wörter zählen und in einem Dictionary speichern
    word_dict = {}
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    
    print(sentence)
    print(word)
    return

word_count()