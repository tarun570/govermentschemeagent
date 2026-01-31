from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .db import Base, engine, SessionLocal
from .models import Scheme
from .crud import load_schemes_from_json
from .vector_store import build_faiss_index, search

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup():
    db = SessionLocal()

    if db.query(Scheme).count() == 0:
        load_schemes_from_json(db, "data/schemes.json")

    schemes = db.query(Scheme).all()
    if schemes:
        build_faiss_index(schemes)

    db.close()


@app.get("/schemes")
def get_schemes(db: Session = Depends(get_db)):
    return db.query(Scheme).all()


@app.get("/ai-search")
def ai_search(q: str):
    return search(q)
