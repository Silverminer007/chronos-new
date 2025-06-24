from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.models.event_instance_overview import EventInstanceOverview

def get_project_events(user_id: int, db: Session):
    subquery_teams = db.query(EventInstanceOverview).filter(
        EventInstanceOverview.calendar.in_(
            db.query(text("pt.calendar_id"))
            .from_statement(text("""
                SELECT pt.calendar_id
                FROM project_team pt
                JOIN project_team_member ptm ON pt.id = ptm.project_team_id
                WHERE ptm.user_id = :uid
            """)).params(uid=user_id)
        )
    )

    subquery_projects = db.query(EventInstanceOverview).filter(
        EventInstanceOverview.calendar.in_(
            db.query(text("p.calendar_id"))
            .from_statement(text("""
                SELECT p.calendar_id
                FROM project p
                JOIN project_participant pp ON p.id = pp.project_id
                JOIN user_account ua ON ua.person_id = pp.person_id
                WHERE ua.id = :uid
            """)).params(uid=user_id)
        )
    )

    return subquery_teams.union_all(subquery_projects).subquery()
