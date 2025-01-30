from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session
import pandas as pd
from compartidos.database import SessionLocal, init_db
from compartidos.models import PostcodeEntry
from schemas import UploadResponse

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db() 

@app.get("/")
def home():
    return {"message": "Microservicio Uploader funcionando!"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload/", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)

    column_map = {"lat": "latitude", "lon": "longitude"}
    df.rename(columns=column_map, inplace=True)

    if "latitude" not in df.columns or "longitude" not in df.columns:
        return {"message": "Formato incorrecto. Se requieren columnas 'latitude' y 'longitude'."}

    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)

    try:
        entries = [
            PostcodeEntry(latitude=float(row["latitude"]), longitude=float(row["longitude"]))
            for _, row in df.iterrows()
        ]
        db.bulk_save_objects(entries)
        db.commit()
        return {"message": "Archivo procesado correctamente", "rows_processed": len(entries)}
    
    except Exception as e:
        db.rollback()
        return {"message": f"Error al procesar el archivo: {str(e)}", "rows_processed": 0}

if __name__ == "__main__":
    init_db()
