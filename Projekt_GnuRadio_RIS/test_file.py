import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from Controller import Controller

app = FastAPI()

@app.get("/")
async def read_root(request: Request):
    return {"Value": "2137"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)