import re
from collections import defaultdict
import matplotlib.pyplot as plt

with open("to_parse.txt") as file:
    text = file.read()

phrase_pattern = re.compile(r"\[(.+?)\](.+?)\[конец\]", re.DOTALL)

matches = phrase_pattern.findall(text)


characters = {"Иисус", "Луций", "Понтий Пилат", "Ирод Антипа", "Варавва", "Иоанн Креститель"}
data = defaultdict(list)
for character, phrase in filter( (lambda m: m[0] in characters), matches):
    data[character].append(phrase)

amount = 0
for character in data:
    charlen = 0
    for phrase in data[character]:
        charlen += len(phrase)
        amount += len(phrase)
    data[character] = charlen

for character in data:
    data[character] = (data[character] / amount) * 100
    print(character, data[character])

plt.pie([v for v in data.values()], labels=data)
plt.show()
