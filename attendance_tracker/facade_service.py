import datetime
import requests
from mysql_repository import * 
import time
import threading
from datetime import datetime, timedelta
from fastapi import FastAPI

membership_url = "http://localhost:5005/api/membershiptypes/"
membership_type_url = "http://localhost:5005/api/membershiptypes/id/"
DISCOUNT_URL = "http://localhost:5005/api/discount/"
GET_DISCOUNT_URL = "http://localhost:5005/api/discount/user/"


app = FastAPI()


def user_session_time_start(usr_id):
    start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    add_visit_start_dtime(usr_id, start)

def user_session_time_end(usr_id):
    end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    add_visit_end_dtime(usr_id, end)

def send_discount_usr():
    records = get_last_visits_end_time()
    current_time = datetime.now()
    print("discount sending")
    for key in records.keys():
        if if_discount(key) == False:
            if current_time - records[key] > timedelta(days=20):
                discount = 15.0
                request = {
                "UserId": f"{key}",
                "Percentage": str(discount),
                "StartDate": f"{current_time}",
                "EndDate": f"{current_time + timedelta(weeks=8)}",
                "IsActive": True
                }
                requests.post(DISCOUNT_URL, json = request)
                print("Discount request sent")

def if_discount(usr_id):
    print("USER ID = ", usr_id)
    response = requests.get(GET_DISCOUNT_URL+f"{usr_id}")
    if response.status_code  == 200:
        if response["isActive"]:
            return True
        else:
            return False
    
def schedule_request():
    while True:
        now = time.time()
        next_day = now + (24 * 60 * 60) 
        remaining_time = next_day % now
        time.sleep(remaining_time)
        send_discount_usr()

