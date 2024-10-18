from fastapi import FastAPI,Request,Depends,Query,Body
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from models_for_endpoints import MessageRequest
from typing import List
from contextlib import asynccontextmanager
from db import *
import requests
import asyncio



    
queue:List[MessageRequest] = []

@asynccontextmanager
async def lifespan(engine_app):
    asyncio.create_task(recv_msg_from_queue())
    yield 

async def recv_msg_from_queue():
    while True:
        if queue:
            message = queue[0]
            host = message['target_host']
            port=message['target_port']
            response=requests.post(url=f'http://{host}:{port}')
            if response.status_code==200:
                with open("service_b_log.txt" , "a") as file:
                     file.write(response.text+'\n')
                queue.pop(0)
        await asyncio.sleep(0.1)
                
app=FastAPI(lifespan=lifespan)

#API брокера
@app.get('/queue')
def get_queue():
    if len(queue)==0:
        return JSONResponse(status_code=200,content={"message": "Сообщения отсутсвуют"})
    return queue
#API брокера
@app.post('/queue')
def append_msg(message:MessageRequest):
    queue.append(message)
    return JSONResponse(status_code=200,content={"body":"Сообщение успешно доставлено","status":"OK"})

@app.get('/subscribe')
def subscribe_service(request:Request,session=Depends(get_db)):
        host,port = request.client.host, request.headers.get("X-Source-Port")
        service = session.query(Service).filter(and_(
            Service.host==request.client.host,
            Service.port==port
        )
            ).first()
        response={}
      
        if service is None:
            session.add(Service(host=host,port=port))
            session.commit()
            response["reg_info"]="Регистрация прошла успешно"
        response['client'] = [host,port]
        response["connection"]="Соединение успешно установлено"
        return JSONResponse(status_code=200,content=response)
    
@app.post('/send')
async def send_msg(message:MessageRequest, request:Request, session=Depends(get_db)):
    queue.append(message.model_dump())
    service_a = session.query(Service).filter(Service.host==request.client.host).first()
    service_b = session.query(Service).filter(Service.host== message.target_host).first()
    session.add(Message(command=message.command,
                        device_id=message.device_id,
                        status=message.status,
                        result=message.result, 
                        from_id = service_a.id,
                        to_id =  service_b.id))
    session.commit()
    message.status="Доставлено"
    return JSONResponse(status_code=200,content={"status":"Added","message":message})

@app.get('/services')
def services(session=Depends(get_db)):
    services=session.query(Service).all()
    body=[]
    for service in services:
        body.append(service.__repr__())
    if body:
        return JSONResponse(status_code=200,content=body)
    return JSONResponse(status_code=404,content={"result":"Not Found"})