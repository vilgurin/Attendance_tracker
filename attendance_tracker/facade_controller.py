from fastapi import FastAPI, HTTPException,BackgroundTasks
import requests
import uuid
from pydantic import BaseModel
from facade_service import * 
import threading
import time

app = FastAPI()

class Data(BaseModel):
    usr_id: str

@app.post("/start")
def start_session(msg: Data):
    print("msg = ", msg)
    user_session_time_start(msg.usr_id)

@app.post("/end")
def start_session(msg: Data):
    user_session_time_end(msg.usr_id)

@app.post("/")
async def trigger_scheduled_request(background_tasks: BackgroundTasks):
    start_scheduled_request(background_tasks)
    return {"message": "Scheduled request started."}

def start_scheduled_request(background_tasks: BackgroundTasks):
    thread = threading.Thread(target=schedule_request)
    thread.daemon = True
    thread.start()
    background_tasks.add_task(thread.join)

@app.get("/")
def get_visits():
    records = get_last_visits_end_time()
    print(records)