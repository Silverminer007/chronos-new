from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from app.db.base import Base

class EventInstanceOverview(Base):
    __tablename__ = "event_instance_overview"

    uid = Column(String, primary_key=True)
    id = Column(Integer)
    calendar = Column(Integer)
    calendar_name = Column(Text)
    dtstart = Column(TIMESTAMP)
    dtend = Column(TIMESTAMP)
    summary = Column(Text)
    status = Column(String)
    class_ = Column("class", String)
    transp = Column(String)
    accepted = Column(Integer)
    declined = Column(Integer)
    needs_action = Column(Integer)
