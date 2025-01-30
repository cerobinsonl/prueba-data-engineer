from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session
import pandas as pd
from compartidos.database import SessionLocal, init_db
from compartidos.models import PostcodeEntry
from schemas import UploadResponse
from services import upload_csv, get_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def home():
    return {"message": "Microservicio Uploader funcionando!"}

@app.post("/upload/", response_model=UploadResponse)
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Endpoint para recibir un archivo CSV y procesarlo usando la función de `services.py`.
    """
    return await upload_csv(file, db)

if __name__ == "__main__":
    init_db()