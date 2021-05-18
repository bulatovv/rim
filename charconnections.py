import re
import matplotlib.pyplot as plt

import networkx as nx

from collections import Counter
from itertools import combinations

with open("to_parse.txt") as file:
    text = file.read()

phrase_pattern = re.compile(r"\[(.+?)\](.+?)\[конец\]", re.DOTALL)
gap_pattern = re.compile(r"\[конец\]\n([^\[]{2,}?)\[", re.DOTALL)


gaps = gap_pattern.finditer(text)
phrases = phrase_pattern.finditer(text)

timeline = []
characters = {
        "Иисус", "Саломея", "Иоанн Креститель", "Иродиана",
        "Варавва", "Иуда", "Понтий Пилат", "Мария", "Иосиф",
        "Каиафа", "Луций", "Ирод Антипа", "Ирод", "Магдалина"
}
for gap in gaps:
    timeline.append((gap.start(1), "GAP"))
for phrase in phrases:
    if phrase[1] in characters:
        timeline.append((phrase.start(1), phrase[1]))
timeline.sort(key = lambda m: m[0])
print(*timeline, sep='\n')

data = Counter()
group = set()
for pos, label in timeline:
    if label == "GAP":
        data.update(combinations(group, 2))
        group = set()
    else:
        group.add(label)

G = nx.Graph()

for conn in data:
    G.add_edge(*conn, weight = data[conn])

pos = nx.shell_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=0)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2, edge_color="gray")
nx.draw_networkx_labels(G, pos, font_size=15, font_family="sans-serif")

figure = plt.gcf()
figure.set_size_inches(15, 15)
plt.axis("off")
plt.savefig("test.png", transparent=True, dpi = 80, bbox_inches = 'tight')
plt.show()
