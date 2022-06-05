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

for d in data:
    try:
        book = d["name"]
        for ic, chater in enumerate(d["chapters"]):
            for iv, verse in enumerate(chater):
                n_chater = ic + 1
                n_verse = iv + 1
                payload = dict(
                    book=book,
                    verse=n_verse,
                    chater=n_chater,
                    text=chater[iv]
                )
                mongoInstance.set(
                    data=payload
                )
                print("%s %s:%s %s - saved." % (book, n_chater, n_verse, chater[iv]))
    except IndexError:
        continue
