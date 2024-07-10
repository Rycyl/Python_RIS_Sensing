import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from RIS import RIS
from Controller import Controller
import os
from enum import Enum

# Pre definowane porty - do zrobienia jak bedzie czas / potrzeba
# def get_ports():
#     if os.name == 'posix':
#         ports = [f"/dev/ttyUSB{i}" for i in range(10)]
#     else:
#         ports = [f"COM{i}" for i in range(10)]

RIS_list = {}

Con = Controller()

app = FastAPI()

@app.post("/raport")
async def data_receive(request: Request):
    data = await request.json()
    Con.save_raport(data)
    #print(data)
    return data

@app.post("/power_reading")
async def data_receive(request: Request):
    data = await request.json()
    Con.save_power_reading(data)
    #print(data)
    return data

@app.get("/connect_RIS")
async def connect_RIS(id: int, port: str):
    RIS_list["RIS_No_{id}"] = Con.init_ris(port, id)
    return RIS_list["RIS_No_{id}"]

@app.post("/set_pattern")
async def set_pattern(id: int, pattern: str):
    if Con.set_pattern(RIS_list["RIS_No_{id}"], pattern):
        return JSONResponse(content={"status": "OK"})
    else:
        return JSONResponse(content={"status": "ERROR"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)