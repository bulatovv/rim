import matplotlib.pyplot as plt
import csv

from collections import Counter

sources = ["Мф", "Мк", "Лк","Ин"]
data = Counter()
with open('timecodes.csv', newline='') as csvfile:
    timecodes = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    
    for row in timecodes:
        data.update(filter((lambda s: s in row["src"]), sources))
print(data)

plt.pie([v for v in data.values()], labels=data)
plt.show()
