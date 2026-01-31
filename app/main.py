print("FINAL MAIN LOADED")

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pathlib import Path

from .db import Base, engine, SessionLocal
from .models import Scheme, User, BusinessProfile
from .crud import (
    load_schemes_from_json,
    create_user, get_users, get_user, delete_user,
    create_business, get_businesses, get_business, delete_business,
    get_schemes, get_scheme
)
from .vector_store import build_faiss_index, search

BASE_DIR = Path(__file__).resolve().parent.parent

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
        load_schemes_from_json(db, BASE_DIR / "data" / "schemes.json")

    schemes = db.query(Scheme).all()
    if schemes:
        build_faiss_index(schemes)

    db.close()


# ---------------- Schemes ----------------

# @app.get("/schemes")
# def get_all_schemes(db: Session = Depends(get_db)):
#     return get_schemes(db)

@app.get("/schemes")
def get_all_schemes(db: Session = Depends(get_db)):

    schemes = get_schemes(db)

    return [
        {
            "id": s.id,
            "name": s.name,
            "benefits": s.benefits,
            "eligibility": s.eligibility
        }
        for s in schemes
    ]


# @app.get("/schemes/{scheme_id}")
# def get_single_scheme(scheme_id: int, db: Session = Depends(get_db)):
#     return get_scheme(db, scheme_id)


@app.get("/schemes/{scheme_id}")
def get_single_scheme(scheme_id: int, db: Session = Depends(get_db)):

    s = get_scheme(db, scheme_id)

    if not s:
        return None

    return {
        "id": s.id,
        "name": s.name,
        "benefits": s.benefits,
        "eligibility": s.eligibility
    }



# ---------------- Users ----------------

@app.post("/users")
def create_user_api(
    name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    return create_user(db, name, email, password)


# @app.get("/users")
# def get_all_users(db: Session = Depends(get_db)):
#     return get_users(db)


@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):

    users = get_users(db)

    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "password": u.password
        }
        for u in users
    ]



# @app.get("/users/{user_id}")
# def get_single_user(user_id: int, db: Session = Depends(get_db)):
#     return get_user(db, user_id)


@app.get("/users/{user_id}")
def get_single_user(user_id: int, db: Session = Depends(get_db)):

    u = get_user(db, user_id)

    if not u:
        return None

    return {
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "password": u.password
    }




@app.delete("/users/{user_id}")
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)


# ---------------- Businesses ----------------

@app.post("/businesses")
def create_business_api(
    business_name: str,
    description: str,
    owner_id: int,
    db: Session = Depends(get_db)
):
    return create_business(db, business_name, description, owner_id)


@app.get("/businesses")
def get_all_businesses(db: Session = Depends(get_db)):
    return get_businesses(db)


@app.get("/businesses/{business_id}")
def get_single_business(business_id: int, db: Session = Depends(get_db)):
    return get_business(db, business_id)


@app.delete("/businesses/{business_id}")
def delete_business_api(business_id: int, db: Session = Depends(get_db)):
    return delete_business(db, business_id)


# ---------------- AI Search ----------------

@app.get("/ai-search")
def ai_search(q: str):
    return search(q)
