from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.models.company import Company

router = APIRouter()


@router.get("/companies")
def list_companies():

    db: Session = SessionLocal()

    companies = db.query(Company).all()

    result = []

    for company in companies:

        result.append({
            "id": company.id,
            "name": company.name
        })

    return result