import re
from collections import defaultdict
import matplotlib.pyplot as plt

with open("to_parse.txt") as file:
    text = file.read()

phrase_pattern = re.compile(r"\[(.+?)\](.+?)\[конец\]", re.DOTALL)

matches = phrase_pattern.findall(text)


characters = {
        "Иисус", "Луций", "Понтий Пилат",
        "Ирод Антипа", "Варавва", "Иоанн Креститель"
}

data = defaultdict(list)
for character, phrase in filter((lambda m: m[0] in characters), matches):
    data[character].append(phrase)

amount = 0
for character in data:
    charlen = 0
    for phrase in data[character]:
        charlen += len(phrase)
        amount += len(phrase)
    data[character] = charlen


colors = ["#c43d16", "#fd9a7e", "#edc596", "#fcb500", "#dc6d02", "#E97D01"]
fig1, ax1 = plt.subplots()
patches, texts, autotexts = ax1.pie(
    [v for v in data.values()],
    labels=data, colors=colors, autopct='%1.1f%%', startangle=90
)
for text in texts:
    text.set_color("#555")
for autotext in autotexts:
    autotext.set_color('#555')
ax1.axis('equal')
plt.savefig("amount.png", transparent=True, dpi=260)
plt.show()
