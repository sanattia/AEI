import os

from clp3 import clp

i = 1
texts_formatted = {}
texts_formatted_by_words = {}


def processText(text):
    text_list = text.split('.')
    text_list_formatted = []
    word_list_formatted = []

    for sentence in text_list:
        word_list = [single_word for single_word in sentence.split() if single_word]
        text_list_formatted.append(sentence.strip())
        if word_list:
            word_list_formatted.append(word_list)

    return text_list_formatted, word_list_formatted


for filename in os.listdir("teksty"):
    index = os.path.basename(filename)
    with open(os.path.join("teksty", filename), 'r') as f:
        text = f.read()
        texts_formatted[index], texts_formatted_by_words[index] = processText(text)


def getSentence(word):
    result = []

    for dict_key, sentences in texts_formatted.items():
        for index, sentence in enumerate(sentences):
            words = sentence.split()
            if any(clp(item) == clp(word) == [] and item == word or set(clp(item)) == set(clp(word)) != [] for item in
                   words):
                result.append([dict_key, index, sentence])

    return result


def getSentenceStats(searched_stats):
    for dict_key, index, sentence in searched_stats:
        print("Tekst {}, zdanie {}: {}.\n".format(dict_key, index, sentence))


def getNeighboor(word):
    texts_with_words_names = []
    result = []

    for dict_key in texts_formatted_by_words.keys():
        for sentence in texts_formatted_by_words[dict_key]:
            for index, iterated_word in enumerate(sentence):
                if (clp(iterated_word) == [] and clp(word) == [] and word == iterated_word) \
                        or (set(clp(iterated_word)) == set(clp(word)) and clp(iterated_word) != [] and clp(word) != []):
                    texts_with_words_names.append(dict_key)
                    start_neighbour = index - 4
                    end_neighbour = index + 5

                    if start_neighbour < 0:
                        start_neighbour = 0
                    if end_neighbour > len(sentence):
                        end_neighbour = len(sentence)

                    result.append([dict_key, sentence[start_neighbour:end_neighbour]])

    return word, set(texts_with_words_names), result


def getNeighboorStats(searched_stats):
    print('Wyraz ' + searched_stats[0] + ' znajduje się w tekstach:')
    print(searched_stats[1])
    for item in searched_stats[2]:
        sentence = ''
        for word in item[1]:
            sentence += word + ' '
        print('Tekst ' + item[0] + ': ' + sentence)


getSentenceStats(getSentence('scenariusz'))

getNeighboorStats(getNeighboor('małe'))
