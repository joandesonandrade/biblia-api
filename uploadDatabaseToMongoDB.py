from util import mongodb
from ujson import loads, JSONDecodeError
from os import path
from pathlib import Path
from dotenv import dotenv_values
from os import environ


class Setting:
    def __init__(self):
        pass

    def getEnvironment(self) -> dict:
        Env = dotenv_values(".env")
        if len(environ) > 0:
            Env.update(environ)
        return Env


Env = Setting().getEnvironment()

print("start upload...")

print("check mongodb connection...")

try:
    mongoInstance = mongodb.MongoDB(Env=Env)
    mongoInstance.getDB()
except Exception as e:
    raise Exception("Error: {}".format(e))

if not path.isfile(Path("database/data.json")):
    raise FileExistsError("banco de dados não foi encontrado...")


print("opening database.json...")

with open(Path("database/data.json"), "r", encoding="utf-8-sig") as rf:
    data = rf.read()
    rf.close()


print("data size: {:.2f}MB".format(len(data) / 1024 / 1024))

print("trying data parse...")

try:
    data = loads(data)
except JSONDecodeError:
    raise JSONDecodeError("banco de dados não é um JSON válido.")

print("ok!")

print("migrate data to mongodb...")

books = list()

for d in data:
    try:
        book = d["name"]
        abbrev = d["abbrev"]
        mx_verse = 0
        n_chapter = 0
        chapters = {}
        for ic, chapter in enumerate(d["chapters"]):
            for iv, verse in enumerate(chapter):
                mx_verse += 1
                n_chapter = ic + 1
                n_verse = iv + 1
                payload = dict(
                    book=book,
                    abbrev=abbrev,
                    verse=n_verse,
                    chapter=n_chapter,
                    text=chapter[iv]
                )
                mongoInstance.set(
                    data=payload
                )
                print("%s %s:%s %s - saved." % (book, n_chapter, n_verse, chapter[iv]))
            chapters[str(n_chapter)] = {
                "verses": mx_verse
            }
            mx_verse = 0
        books.append({
            "book": book,
            "abbrev": abbrev,
            "chapters": chapters
        })
        chapters = {}
    except IndexError:
        continue

print("data uploaded!")

print("migrate books and abbrov to mongodb...")
for book in books:
    mongoInstance.set(
        data=book,
        collection="books"
    )

print("[+] successful")