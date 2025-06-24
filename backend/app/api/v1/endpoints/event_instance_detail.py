from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud.event_instance_detail import get_event_instance_with_attendees

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/event-instance/{instance_id}", response_model=dict)
def read_event_instance(instance_id: int, db: Session = Depends(get_db)):
    data = get_event_instance_with_attendees(instance_id, db)
    if not data:
        raise HTTPException(status_code=404, detail="Event instance not found")
    return data
