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
