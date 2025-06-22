import pymysql
import hashlib
from radicale.storage import BaseStorage, BaseCollection
from radicale.item import Item
from icalendar import Calendar, Event
from datetime import datetime


class Storage(BaseStorage):
    def __init__(self, configuration, *args, **kwargs):
        self.configuration = configuration

        # Versuche path und principal aus args zu extrahieren
        self.path = None
        self.principal = None

        if len(args) == 2:
            # z.B. (path, principal)
            self.path = args[0]
            self.principal = args[1]
        elif len(args) == 3:
            # z.B. (name, path, principal)
            self.path = args[1]
            self.principal = args[2]

        # Falls in kwargs vorhanden
        self.path = self.path or kwargs.get("path")
        self.principal = self.principal or kwargs.get("principal")

        # Falls immer noch None, Default-Werte setzen
        self.path = self.path or ""
        self.principal = self.principal or ""

        self.db = pymysql.connect(
            host="mysql",
            user="radicale",
            password="secret",
            database="calendar",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_collection(self, path, items=None):
        return MySQLCollection(self.db, path, self.principal)


class MySQLCollection(BaseCollection):
    def __init__(self, db, path, principal):
        self.db = db
        self.path = path
        self.principal = principal
        self._items = None

    def list(self):
        return [item.href for item in self.items()]

    def items(self):
        if self._items is not None:
            return self._items

        user = self.principal

        with self.db.cursor() as cursor:
            cursor.execute("""
                SELECT d.id, d.title, d.start, d.end, d.notes
                FROM date d
                JOIN gruppe_participants gp ON d.group_id = gp.gruppe_id
                JOIN person p ON gp.person_id = p.id
                WHERE p.username = %s
            """, (user,))

            rows = cursor.fetchall()

        self._items = [self._to_item(row) for row in rows]
        return self._items

    def get(self, href):
        id_ = self._id_from_href(href)

        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM date WHERE id = %s", (id_,))
            row = cursor.fetchone()

        if not row:
            return None

        return self._to_item(row)

    def upload(self, href, item, etag=None):
        id_ = self._id_from_href(href)
        calendar = Calendar.from_ical(item.data)
        vevent = next(component for component in calendar.walk() if component.name == "VEVENT")

        with self.db.cursor() as cursor:
            cursor.execute("""
                UPDATE date SET
                    title = %s,
                    start = %s,
                    end = %s,
                    notes = %s
                WHERE id = %s
            """, (
                str(vevent.get("summary")),
                vevent.decoded("dtstart").isoformat(),
                vevent.decoded("dtend").isoformat(),
                str(vevent.get("description")),
                id_
            ))
        self.db.commit()
        return self.get(href)

    def delete(self, href, etag=None):
        id_ = self._id_from_href(href)
        with self.db.cursor() as cursor:
            cursor.execute("DELETE FROM date WHERE id = %s", (id_,))
        self.db.commit()

    def _to_item(self, row):
        cal = Calendar()
        event = Event()
        event.add("uid", str(row["id"]))
        event.add("summary", row.get("title") or "No Title")
        event.add("dtstart", row["start"])
        event.add("dtend", row["end"])
        event.add("description", row.get("notes") or "")
        event.add("dtstamp", datetime.utcnow())
        cal.add_component(event)

        ical_data = cal.to_ical()  # bytes
        etag = hashlib.sha1(ical_data).hexdigest()
        href = f"/api/v1/ical/date/{row['id']}.ics"

        return Item(href=href, data=ical_data, etag=etag)

    def _id_from_href(self, href):
        return int(href.strip("/").split("/")[-1].replace(".ics", ""))
