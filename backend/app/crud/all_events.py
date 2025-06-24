from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.models.event_instance_overview import EventInstanceOverview


def get_all_visible_events(user_id: int, db: Session):
    base_query = db.query(EventInstanceOverview).from_statement(text("""
                                                                     SELECT DISTINCT eio.*
                                                                     FROM event_instance_overview eio
                                                                              JOIN calendar c ON c.id = eio.calendar
                                                                              LEFT JOIN calendar_share cs ON cs.calendar_id = c.id
                                                                              LEFT JOIN project p ON p.calendar_id = c.id
                                                                              LEFT JOIN project_participant pp ON pp.project_id = p.id
                                                                              LEFT JOIN user_account ua_p ON ua_p.person_id = pp.person_id
                                                                              LEFT JOIN project_team pt ON pt.calendar_id = c.id
                                                                              LEFT JOIN project_team_member ptm ON ptm.project_team_id = pt.id
                                                                     WHERE c.owner = :uid
                                                                        OR (cs.user_id = :uid AND cs.classification > eio.class)
                                                                        OR ua_p.id = :uid
                                                                        OR ptm.user_id = :uid
                                                                     """)).params(uid=user_id)

    return base_query
