import matplotlib.pyplot as plt
import csv

from collections import Counter

sources = ["Мф", "Мк", "Лк","Ин"]
data = Counter()
with open('full_timecodes.csv', newline='') as csvfile:
    timecodes = csv.DictReader(csvfile, delimiter=',', quotechar='"')    
    for row in timecodes:
        data.update(filter((lambda s: s in row["src"]), sources))

colors = ["#c43d16", "#fd9a7e", "#edc596", "#fcb500", "#dc6d02", "#E97D01"]
fig1, ax1 = plt.subplots()
patches, texts, autotexts = ax1.pie([v for v in data.values()], labels=data,colors = colors, autopct='%1.1f%%', startangle=90)
for text in texts:
    text.set_color("#555")
for autotext in autotexts:
    autotext.set_color('#555')
ax1.axis('equal')  
plt.savefig("citations.png", transparent=True, dpi = 260)
plt.show()
