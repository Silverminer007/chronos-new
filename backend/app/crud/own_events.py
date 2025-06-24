from sqlalchemy.orm import Session
from app.models.event_instance_overview import EventInstanceOverview

def get_own_events(user_id: int, db: Session):
    return db.query(EventInstanceOverview).filter(
        EventInstanceOverview.calendar.in_(
            db.query("id").from_statement(
                text("SELECT id FROM calendar WHERE owner = :uid")
            ).params(uid=user_id)
        )
    )
