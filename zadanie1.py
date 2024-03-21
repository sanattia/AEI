import os
from clp3 import clp

diacriticalMarks = {
    'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
    'a': 'ą', 'c': 'ć', 'e': 'ę', 'l': 'ł', 'n': 'ń', 'o': 'ó', 's': 'ś', 'z': 'ż', 'z': 'ź'
}


def getWords(word):
    wordArray = []
    for letter in word:
        variations = []
        for key, value in diacriticalMarks.items():
            if letter == value:
                variations.append(key)
        variations.append(letter)
        wordArray.append(variations)

    def generateComb(arrays):
        if not arrays:
            return [[]]

        combinations = []
        first = arrays[0]
        remaining = arrays[1:]

        for item in first:
            for comb in generateComb(remaining):
                combinations.append([item] + comb)

        return combinations

    letters_combinations = generateComb(wordArray)
	
    # zmien kombinacje na słowa do sprawdzenia w clp
    comb = []
    for tuple_letters in letters_combinations:
        possible_word = ''.join(tuple_letters)
        comb.append(possible_word)

    # sprzwadź clp
    ids = []
    for item in comb:
        item_clp = clp(item)
        if len(item_clp):
            ids += item_clp
        return ids


print(getWords("wąż"))
