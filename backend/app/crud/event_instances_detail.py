from sqlalchemy.orm import Session
from sqlalchemy import select, join
from app.models import event_instances, events, attendees, user_account, person

def get_event_instance_with_attendees(instance_id: int, db: Session):
    # Get the event instance and event data
    instance = db.execute(
        select(event_instances, events)
        .join(events, events.c.uid == event_instances.c.event_uid)
        .where(event_instances.c.id == instance_id)
    ).first()

    if not instance:
        return None

    instance_data = dict(instance._mapping[event_instances])
    event_data = dict(instance._mapping[events])
    combined = {**instance_data, **event_data}

    # Get attendees
    result = db.execute(
        select(
            attendees.c.partstat.label("status"),
            person.c.id,
            person.c.firstName,
            person.c.lastName
        )
        .select_from(
            attendees.join(user_account, user_account.c.id == attendees.c.attendee)
                     .join(person, person.c.id == user_account.c.person_id)
        )
        .where(attendees.c.event_instance_id == instance_id)
    ).all()

    combined["attendees"] = [dict(row._mapping) for row in result]

    return combined
