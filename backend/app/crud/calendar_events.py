from sqlalchemy.orm import Session
from app.models.event_instance_overview import EventInstanceOverview

def get_events_by_calendar(calendar_id: int, db: Session):
    return db.query(EventInstanceOverview).filter(
        EventInstanceOverview.calendar == calendar_id
    )
