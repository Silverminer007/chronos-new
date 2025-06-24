from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from collections import defaultdict
from app.db.session import SessionLocal
from app.models.event_instance_overview import EventInstanceOverview
from app.schemas.event_instance_overview import EventInstanceSchema
from app.crud.own_events import get_own_events
from app.db.filters import parse_filters

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/own-events/{user_id}", response_model=dict)
def read_own_events(user_id: int, request: Request, db: Session = Depends(get_db)):
    base_query = get_own_events(user_id, db)
    filters = parse_filters(EventInstanceOverview, request.query_params)
    results = base_query.filter(filters).all()

    grouped = defaultdict(list)
    for row in results:
        grouped[row.calendar_name or "Unbekannt"].append(EventInstanceSchema.from_orm(row).dict())

    return {"data": [{"calendar_name": name, "events": events} for name, events in grouped.items()]}
