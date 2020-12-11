from fastapi import FastAPI, Request, File, UploadFile
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import numpy as np
import os
import io
import cv2
import pytesseract


class ImageType(BaseModel):
 url: str

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def read_img(img):
 text = pytesseract.image_to_string(img)
 return(text)

@app.post("/extract_text") 
async def extract_text(request: Request, file: bytes = File(...)):
    label =''
    if request.method == "POST":
        image_stream = io.BytesIO(file)
        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        label =  read_img(frame)
        return label
    return templates.TemplateResponse("index.html", {"request": request, "label": label})