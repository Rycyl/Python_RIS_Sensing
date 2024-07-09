import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/receive")
async def data_receive(request: Request):
    data = await request.json()
    print(data)
    return {"data": data}
    #return {"data": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)