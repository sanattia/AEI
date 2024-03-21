import os
from collections import Counter

from clp3 import clp
import re
from flask import Flask, \
    render_template, \
    redirect

app = Flask(__name__)

rules = {
    'Cel': {"przedmiot", "nagroda", "postać"},
    'Zdarzenie': {"hazard", "hazardowy", "mikropłatność"},
    'Obiekt': {"pieniądz", "dziecko", "gracz"},
    'Sprawca': {"gra"},
    'Narzędzie': {"loot", "box", "lootbox", "lootboxów", "lootboxy", "skrzynka"}
}

grades = {
    'Cel': '0.1',
    'Zdarzenie': '0.2',
    'Obiekt': '0.2',
    'Sprawca': '0.2',
    'Narzędzie': '0.3',
    ('Cel', 'Zdarzenie'): '0.5',
    ('Cel', 'Obiekt'): '0.5',
    ('Cel', 'Sprawca'): '0.5',
    ('Cel', 'Narzędzie'): '0.5',
    ('Zdarzenie', 'Obiekt'): '0.5',
    ('Zdarzenie', 'Sprawca'): '0.6',
    ('Zdarzenie', 'Narzędzie'): '0.6',
    ('Obiekt', 'Sprawca'): '0.5',
    ('Obiekt', 'Narzędzie'): '0.6',
    ('Sprawca', 'Narzędzie'): '0.8',
    ('Cel', 'Zdarzenie', 'Obiekt'): '0.8',
    ('Cel', 'Zdarzenie', 'Sprawca'): '0.8',
    ('Cel', 'Zdarzenie', 'Narzędzie'): '0.8',
    ('Cel', 'Obiekt', 'Sprawca'): '0.6',
    ('Cel', 'Obiekt', 'Narzędzie'): '0.8',
    ('Cel', 'Sprawca', 'Narzędzie'): '0.85',
    ('Zdarzenie', 'Obiekt', 'Sprawca'): '0.75',
    ('Zdarzenie', 'Obiekt', 'Narzędzie'): '0.8',
    ('Zdarzenie', 'Sprawca', 'Narzędzie'): '0.8',
    ('Obiekt', 'Sprawca', 'Narzędzie'): '0.8',
    ('Cel', 'Zdarzenie', 'Obiekt', 'Sprawca'): '0.8',
    ('Cel', 'Zdarzenie', 'Obiekt', 'Narzędzie'): '0.8',
    ('Cel', 'Zdarzenie', 'Sprawca', 'Narzędzie'): '0.95',
    ('Cel', 'Obiekt', 'Sprawca', 'Narzędzie'): '0.95',
    ('Zdarzenie', 'Obiekt', 'Sprawca', 'Narzędzie'): '0.95',
    ('Cel', 'Zdarzenie', 'Obiekt', 'Sprawca', 'Narzędzie'): '1.0',
}


def getTexts():
    texts = {}
    directory_path = os.path.join(os.getcwd(), "teksty")
    for filename in os.listdir(directory_path):
        index = os.path.basename(filename)
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r') as f:
            text = f.read()
            texts[index] = text
    return texts


# słowa najczsciej uzywane - lista frekwencyjna #
def getWords():
    folder_path = "teksty"
    file_list = [filename for filename in os.listdir(folder_path) if filename.endswith(".txt")]

    cnt = Counter()

    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        file = open(file_path, "rt")
        stringFile = file.read()
        file.close()

        word_list = stringFile.split()

        for word in word_list:
            word = re.sub(r"[^a-zA-Ząćęłóśżź_]", '', word)
            if word:
                cnt[word] += 1

    myString = ''
    counter = 0
    for key in cnt.most_common():
        counter += 1
        myString += str(counter) + ' '
        newWord = str(key)
        newWord = re.sub(r"[^a-zA-Ząćęłóśżź0-9_]", ' ', newWord)
        myString += newWord + '\n'

    return myString


def getResults(texts, rules, grades):
    allResults = []
    for text in texts.values():
        editedTextsDict = {}
        words = text.split()

        for word in words:
            if clp(word):
                # jeśli istnieje w clp#
                word_id = sorted(clp(word), key=lambda x: clp.label(x))[0]
                editedTexts = clp.bform(word_id).split()[0]
                # dla każdej zasady sprawdzam#
                for rule in rules.values():
                    # jeśli słowo istnieje w zasadach ide dalej#
                    if editedTexts in rule:

                        # dodaje do słownika moich zasad#
                        for key, checks in rules.items():
                            if editedTexts in checks:
                                # dodaje pattern żeby nie robił się błąd że np podkreśla gracz w graczom#
                                pattern = r"\b{}\b".format(re.escape(word))
                                text = re.sub(pattern, '<span class="' + key + '">' + word + '</span>', text)
                                if key in editedTextsDict:
                                    # klucz istnieje
                                    if editedTexts not in editedTextsDict[key]:
                                        editedTextsDict[key].append(editedTexts)
                                else:
                                    # klucz nie istnieje
                                    editedTextsDict[key] = [editedTexts]
            else:
                # to samo ale dla lootboxów#
                for rule in rules.values():
                    # jeśli słowo istnieje w zasadach ide dalej#
                    if word in rule:

                        # dodaje do słownika moich zasad#
                        for key, checks in rules.items():
                            if word in checks:
                                # dodaje pattern żeby nie robił się błąd że np podkreśla gracz w graczom#
                                pattern = r"\b{}\b".format(re.escape(word))
                                text = re.sub(pattern, '<span class="' + key + '">' + word + '</span>', text)
                                if key in editedTextsDict:
                                    # klucz istnieje
                                    if word not in editedTextsDict[key]:
                                        editedTextsDict[key].append(word)
                                else:
                                    # klucz nie istnieje
                                    editedTextsDict[key] = [word]

        editedKeys = list(editedTextsDict.keys())
        matchedGrade = None
        # sprawdzam, czy zgadza sie lista kluczy z editedTextsDict z grades, jak tak to to moja ocena#
        for gradeKey in grades:
            if set(gradeKey) == set(editedKeys):
                matchedGrade = float(grades[gradeKey])
                break
            else:
                # dodane, żeby można było sortować#
                matchedGrade = 0.0

        allResults.append((text, editedTextsDict, matchedGrade))

    return allResults


results = getResults(getTexts(), rules, grades)
textsFreq = getWords()


@app.route('/')
def index():
    global results
    # sortowanie wyników#
    sorted_results = sorted(results, key=lambda x: x[2], reverse=True)
    return render_template('index.html', results=sorted_results)


@app.route('/form')
def form():
    global textsFreq
    global rules
    return render_template('form.html', rules=rules, textsFreq=textsFreq)


@app.route('/reguly')
def reguly():
    global highlights
    return render_template('reguly.html', grades=grades)


@app.route('/main')
def main():
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5244, debug=True)
