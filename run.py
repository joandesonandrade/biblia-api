from dotenv import dotenv_values
from os import environ
from uvicorn import run as uvicornrun
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from util import mongodb
from random import randint


class Setting:
    def __init__(self):
        pass

    def getEnvironment(self) -> dict:
        Env = dotenv_values(".env")
        if len(environ) > 0:
            Env.update(environ)
        return Env


settings = Setting()
Env = settings.getEnvironment()
app = FastAPI()


def resposeSuccess(data: dict = None) -> JSONResponse:
    return JSONResponse(content=dict(success=True, data=data), status_code=200)


def resposeError(msg: str = None, code=404) -> JSONResponse:
    return JSONResponse(content=dict(success=False, msg=msg), status_code=code)


@app.get("/random")
async def random() -> JSONResponse:
    instance = mongodb.MongoDB(Env=Env)
    results = instance.findAll(
        filter={},
        collection="books"
    )

    book = results[randint(0, len(results) - 1)]
    chapters = book[0]["chapters"]
    abbrev = book[0]["abbrev"]
    chapter = randint(1, len(chapters))
    verse = randint(1, chapters[str(chapter)]["verses"])

    result = instance.findOne(
        filter=dict(
            abbrev=abbrev,
            chapter=chapter,
            verse=verse
        ),
        collection="biblia"
    )

    result["text"] = str(result["text"]).replace("\"", "").replace("\n", "")

    return resposeSuccess(data=result)


@app.get("/books")
async def books() -> JSONResponse:
    instance = mongodb.MongoDB(Env=Env)
    results = instance.findAll(
        filter={},
        collection="books"
    )
    if results:
        return resposeSuccess(data=results)
    return resposeError(msg="not found", code=404)


@app.get('/search/{abbrev}/{chapter}/{verse}')
async def search(abbrev: str = '', chapter: int = 1, verse: int = 1) -> JSONResponse:
    instance = mongodb.MongoDB(Env=Env)
    result = instance.findOne(
        filter=dict(
            abbrev=abbrev,
            chapter=chapter,
            verse=verse
        ),
        collection="biblia"
    )
    instance.close()
    if result:
        return resposeSuccess(data=result)
    return resposeError(msg="not found", code=404)


if __name__ == "__main__":
    uvicornrun(
        app,
        host=Env.get("HTTP_HOST"),
        port=int(Env.get("HTTP_PORT")),
        log_level="info"
    )
