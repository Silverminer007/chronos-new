from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from collections import defaultdict
from app.db.session import SessionLocal
from app.models.event_instance_overview import EventInstanceOverview
from app.schemas.event_instance_overview import EventInstanceSchema
from app.crud.calendar_events import get_events_by_calendar
from app.db.filters import parse_filters

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/calendar-events/{calendar_id}", response_model=dict)
def read_events_by_calendar(calendar_id: int, request: Request, db: Session = Depends(get_db)):
    base_query = get_events_by_calendar(calendar_id, db)
    filters = parse_filters(EventInstanceOverview, request.query_params)
    results = base_query.filter(filters).all()

    grouped = defaultdict(list)
    for row in results:
        grouped[row.calendar_name or "Unbekannt"].append(EventInstanceSchema.from_orm(row).dict())

    return {"data": [{"calendar_name": name, "events": events} for name, events in grouped.items()]}
