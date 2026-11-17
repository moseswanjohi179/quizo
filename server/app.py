import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import fastapi
import uvicorn
import time
import os

from fastapi import FastAPI


os.environ["TZ"] = "Africa/Nairobi"
time.tzset()

app = FastAPI()

@app.get("/")
def hello():
    response = {
        "message":"!!Welcome To Quizo!!",
        "current_time": time.ctime()
    }
    return response

