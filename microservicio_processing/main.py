from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api_consumer  import fetch_postcode
from compartidos.database import SessionLocal, init_db
from compartidos.models import PostcodeEntry

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
