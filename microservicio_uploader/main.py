from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session
import pandas as pd
from compartidos.database import SessionLocal, init_db
from compartidos.models import PostcodeEntry
from schemas import UploadResponse

app = FastAPI()

PROCESSING_SERVICE_URL = "http://microservicio_processing:8001/process_batch/"
BATCH_SIZE = 100

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
    """
    Endpoint para cargar un archivo CSV con coordenadas, almacenarlas en la BD,
    y luego enviarlas en lotes de 100 al microservicio Processing.
    """
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

        coordinates_list = df[["latitude", "longitude"]].to_dict(orient="records")
        total_records = len(coordinates_list)
        batch_responses = []

        for i in range(0, total_records, BATCH_SIZE):
            batch = coordinates_list[i : i + BATCH_SIZE]
            response = requests.post(PROCESSING_SERVICE_URL, json={"coordinates": batch})

            if response.status_code == 200:
                batch_responses.append(response.json())
            else:
                batch_responses.append({"error": f"Fallo en batch {i // BATCH_SIZE}: {response.text}"})

        return {"message": "Archivo procesado correctamente", "rows_processed": len(entries), "processing_response": batch_responses}
    
    except Exception as e:
        db.rollback()
        return {"message": f"Error al procesar el archivo: {str(e)}", "rows_processed": 0}

if __name__ == "__main__":
    init_db()
