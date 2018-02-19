from os.path import join
import sqlite3 as lite
from bs4 import BeautifulSoup

con = lite.connect(join('database', 'database.db'))
cur = con.cursor()

def insert(word, translate):
    cur.execute("INSERT INTO sentences VALUES (NULL, '"+word+"', '"+translate+"', 0);")
    print("INSERT INTO sentences VALUES (NULL, '"+word+"', '"+translate+"', 0);")


with open('1.html') as f:
    lines = f.read()
lines = BeautifulSoup(lines, "lxml").text.split("\n")

for i in range(len(lines)):
    try:
        n = int(lines[i])
        word = lines[i+1]
        description = lines[i+2]
        translate = lines[i+3]
    except IndexError:
        continue
    except ValueError:
        continue

    if n and len(word) > 3 and '[' in description and ']' in description and len(translate) > 3:
        #print(n, word, translate)
        insert(word, translate)

con.close()
#print(lines)