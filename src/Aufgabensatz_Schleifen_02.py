sentence = input("Satz, in dem das längste Wort gesucht wird: ")

# Satz in Wörter aufteilen
list_sentence = sentence.split()

# Das längste Wort finden
longest_word = max(list_sentence, key=len)

# Liste nur mit dem längsten Wort füllen
list_sentence = [longest_word]

print(list_sentence)