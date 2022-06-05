from dotenv import dotenv_values
from os import environ
from numba import jit
from uvicorn import run as uvicornrun
from fastapi import FastAPI
from fastapi.responses import JSONResponse


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


@app.get('/search/{book}/{chater}/{verse}')
def search(book: str = '', chater: int = 1, verse: int = 1) -> JSONResponse:
    ok, info = checkQueryFormat(query)
    if ok:
        return resposeSuccess(data=info)


if __name__ == "__main__":
    uvicornrun(
        app,
        host=Env.get("HTTP_HOST"),
        port=int(Env.get("HTTP_PORT")),
        log_level="info"
    )
