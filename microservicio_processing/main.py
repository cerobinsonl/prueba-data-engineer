from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api_consumer  import fetch_postcode, fetch_postcodes_batch
from compartidos.database import SessionLocal, init_db
from compartidos.models import PostcodeEntry
from pydantic import BaseModel
from typing import List


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Coordinate(BaseModel):
    latitude: float
    longitude: float

class BatchRequest(BaseModel):
    coordinates: List[Coordinate]

@app.post("/update_postcodes/")
def update_postcodes(db: Session = Depends(get_db)):
    """
    Recorre la base de datos en busca de coordenadas sin código postal
    y las procesa una por una llamando a la API externa.
    """
    entries = db.query(PostcodeEntry).filter(PostcodeEntry.postcode == None).all()
    
    if not entries:
        return {"message": "No hay registros pendientes de actualización."}
    
    for entry in entries:
        postcode = fetch_postcode(entry.latitude, entry.longitude)

        if postcode:
            entry.postcode = postcode

    db.commit()
    return {"message": f"Postcodes actualizados para {len(entries)} registros"}


@app.post("/process_batch/")
def process_batch(batch: BatchRequest, db: Session = Depends(get_db)):
    """
    Recibe una lista de coordenadas y realiza una consulta en lote a postcodes.io.
    Luego, actualiza la base de datos con los códigos postales obtenidos.
    """
    if not batch.coordinates:
        return {"message": "No se recibieron coordenadas para procesar."}

    coordinates_list = [(coord.latitude, coord.longitude) for coord in batch.coordinates]

    postcodes_dict = fetch_postcodes_batch(coordinates_list)

    updated_rows = 0
    for (latitude, longitude), postcode in postcodes_dict.items():
        db.query(PostcodeEntry).filter(
            PostcodeEntry.latitude == latitude,
            PostcodeEntry.longitude == longitude
        ).update({"postcode": postcode})
        updated_rows += 1

    db.commit()
    return {"message": f"Postcodes actualizados para {updated_rows} registros"}