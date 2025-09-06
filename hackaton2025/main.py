from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Ubicacion

app = FastAPI()

# Modelo de datos de entrada (lo que manda el navegador)
class Coordenadas(BaseModel):
    latitud: float
    longitud: float

# Dependencia para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para guardar coordenadas
@app.post("/ubicaciones/")
def guardar_ubicacion(coord: Coordenadas, db: Session = Depends(get_db)):
    nueva_ubicacion = Ubicacion(latitud=coord.latitud, longitud=coord.longitud)
    db.add(nueva_ubicacion)
    db.commit()
    db.refresh(nueva_ubicacion)
    return {"id": nueva_ubicacion.id, "latitud": nueva_ubicacion.latitud, "longitud": nueva_ubicacion.longitud}

# Endpoint para consultar todas las ubicaciones guardadas
@app.get("/ubicaciones/")
def obtener_ubicaciones(db: Session = Depends(get_db)):
    return db.query(Ubicacion).all()
