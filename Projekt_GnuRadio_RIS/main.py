import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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
    return JSONResponse(content={"status": Con.init_ris(port, id)})

@app.post("/set_pattern")
async def set_pattern(id: int, pattern: str):
    if Con.set_pattern(id, pattern):
        return JSONResponse(content={"status": f"Pattern {pattern} set successfully"})
    else:
        return JSONResponse(content={"status": "ERROR"})

@app.get("/current_pattern")
async def current_pattern(id: int):
    return JSONResponse(content={"current_pattern": Con.c_pattern(id)})

@app.get("/veryf_pattern")
async def veryf_pattern(id: int):
    return JSONResponse(content={"veryf_pattern": Con.veryfy_pattern(id)})
    
@app.get("/reset")
async def reset(id: int):
    if Con.reset(id):
        return JSONResponse(content={"status": "RIS reset successfully"})
    else:
        return JSONResponse(content={"status": "ERROR"})

@app.post("/set_transmision_parameters")
async def set_transmision_paramiters(feq: float, gain: float, samp_rate: int):
    return JSONResponse(content={"status": Con.set_tran_param(feq, gain, samp_rate)})

@app.get("/send_parameters")
async def send_parameters():
    return JSONResponse(content=Con.send_transmision_params())
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)