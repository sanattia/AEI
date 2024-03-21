import os
import re
from collections import Counter

# Get the list of files in the "teksty" folder
folder_path = "teksty"
file_list = [filename for filename in os.listdir(folder_path) if filename.endswith(".txt")]

cnt = Counter()  # Initialize the counter outside the loop

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

text_file = open("resultss.csv", "w")
text_file.write(myString)
text_file.close()
