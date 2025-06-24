from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from collections import defaultdict
from app.db.session import SessionLocal
from app.models.event_instance_overview import EventInstanceOverview
from app.schemas.event_instance_overview import EventInstanceSchema
from app.crud.project_events import get_project_events
from app.db.filters import parse_filters

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/project-events/{user_id}", response_model=dict)
def read_project_events(user_id: int, request: Request, db: Session = Depends(get_db)):
    base_query = get_project_events(user_id, db)
    from sqlalchemy.orm import aliased
    EIO = aliased(EventInstanceOverview, base_query)

    filters = parse_filters(EIO, request.query_params)
    results = db.query(EIO).filter(filters).all()

    grouped = defaultdict(list)
    for row in results:
        grouped[row.calendar_name or "Unbekannt"].append(EventInstanceSchema.from_orm(row).dict())

    return {"data": [{"calendar_name": name, "events": events} for name, events in grouped.items()]}
