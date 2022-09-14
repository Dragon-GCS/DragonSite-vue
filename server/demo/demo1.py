import uvicorn
from fastapi import FastAPI, Response, Cookie, Depends

app = FastAPI()


async def test_dep(login_require: str) -> str:
    return login_require

@app.get("/")
async def set_cookie(raw: str = 'hello world', dep: str = Depends(test_dep)):
    response = Response(raw + dep)
    return response


if __name__ == '__main__':
    uvicorn.run('demo1:app', reload=True)