import pandas as pd
import requests
from fastapi import UploadFile, Depends
from sqlalchemy.orm import Session
from compartidos.models import PostcodeEntry
from schemas import UploadResponse
from compartidos.database import SessionLocal

PROCESSING_SERVICE_URL = "http://microservicio_processing:8001/process_batch/"
BATCH_SIZE = 100

def get_db():
    """
    Función para obtener una sesión de la base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def upload_csv(file: UploadFile, db: Session):
    """
    Carga un archivo CSV con coordenadas, almacena los datos en la BD
    y los envía en lotes de 100 registros al microservicio Processing.
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
            PostcodeEntry(latitude=row["latitude"], longitude=row["longitude"])
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

        return UploadResponse(
            message="Archivo procesado correctamente",
            rows_processed=len(entries),
            processing_response=batch_responses
        )

    except Exception as e:
        db.rollback()
        return {"message": f"Error al procesar el archivo: {str(e)}", "rows_processed": 0}
