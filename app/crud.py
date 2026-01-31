import json
from .models import Scheme


def load_schemes_from_json(db, path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for s in data:
        obj = Scheme(
            name=s["name"],
            eligibility=s["eligibility"],
            benefits=s["benefits"]
        )
        db.add(obj)

    db.commit()

from .models import User, BusinessProfile, Scheme


# ------------------------
# Users CRUD
# ------------------------

def create_user(db, name, email, password):
    user = User(name=name, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db):
    return db.query(User).all()


def get_user(db, user_id):
    return db.query(User).filter(User.id == user_id).first()


def delete_user(db, user_id):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user


# ------------------------
# Business Profile CRUD
# ------------------------

def create_business(db, business_name, description, owner_id):
    business = BusinessProfile(
        business_name=business_name,
        description=description,
        owner_id=owner_id
    )
    db.add(business)
    db.commit()
    db.refresh(business)
    return business


def get_businesses(db):
    return db.query(BusinessProfile).all()


def get_business(db, business_id):
    return db.query(BusinessProfile).filter(
        BusinessProfile.id == business_id
    ).first()


def delete_business(db, business_id):
    business = get_business(db, business_id)
    if business:
        db.delete(business)
        db.commit()
    return business


# ------------------------
# Schemes CRUD
# ------------------------

def get_schemes(db):
    return db.query(Scheme).all()


def get_scheme(db, scheme_id):
    return db.query(Scheme).filter(Scheme.id == scheme_id).first()
