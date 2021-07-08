from bs4 import BeautifulSoup
import random
import csv

books = {
    "Мф" : "52-matthew.dat",
    "Мк" : "53-mark.dat",
    "Лк" : "54-luke.dat",
    "Ин" : "55-john.dat"
}

VERSES_PATH = "../full_timecodes.csv"
verses = []

def remove_tags(text):
    return BeautifulSoup(text, "html.parser").text

def get_verse(verse: str):
    bookname, rest = verse.split()
    colon = rest.find(":")
    
    chapter, rest = int(rest[:colon]), rest[colon + 1:]

    if rest.find("-") != -1:
        start, end = [int(x) for x in rest.split("-")]
        verse_num = slice(start, end + 1)
    else:
        verse_num = slice(int(rest), int(rest) + 1)

    return " ".join(books[bookname][chapter][verse_num])

def random_verse():
    return random.choice(verses)

for bookname in books:
    with open(books[bookname]) as file:
        books[bookname] = [[""]]
        chapter = 0
        verse = 0
        while (line := file.readline()):
            if line.startswith("#p"):
                continue

            chapter, rest = line[1:line.index(":")], line[line.index(":"):]
            new_chapter = int(line[1:line.index(":")])
            new_verse = int(rest[1:rest.index("#")])

            if chapter != new_chapter:
                chapter = new_chapter
                books[bookname].append([[""]])
            
            start = line.index("#", line.index(":"))
            clean = remove_tags(line[start + 1:-1])

            if verse != new_verse:
                verse = new_verse
                books[bookname][chapter].append(clean)
            else:
                books[bookname][chapter][verse] += ' ' + clean


with open(VERSES_PATH, newline='') as csvfile:
    for row in csv.DictReader(csvfile):
        verses.extend([verse.strip() for verse in row["src"].split(';')])
