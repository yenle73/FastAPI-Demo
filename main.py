'''from model import model_pipeline

from fastapi import FastAPI, UploadFile
import io
from PIL import Image

app = FastAPI()

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.post('/ask')
def ask(text: str, image: UploadFile):
    content = image.file.read()
    image = Image.open(io.BytesIO(content))
    # image = Image(image.file)

    result = model_pipeline(text, image)

    return {'answer': result}'''


import io
from PIL import Image
from fastapi import FastAPI, Form, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model import model_pipeline
import base64


app = FastAPI()

# Sử dụng thư mục 'static' để chứa tệp tĩnh như CSS hoặc JavaScript
app.mount("/static", StaticFiles(directory="static"), name="static")

# Sử dụng Jinja2Templates để render trang HTML
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask(request: Request, text: str = Form(...), image: UploadFile = File(...)):
    content = image.file.read()
    image = Image.open(io.BytesIO(content))

    result = model_pipeline(text, image)
    return templates.TemplateResponse("index.html", {"request": request, "answer": result})
