import psycopg2
from dateutil.rrule import rrulestr
from dateutil.parser import parse
from datetime import datetime, timedelta

DB_CONFIG = {
    "dbname": "dein_datenbankname",
    "user": "dein_user",
    "password": "dein_passwort",
    "host": "localhost",
    "port": "5432"
}

GENERATE_DAYS_AHEAD = 365

def parse_exdates(raw_exdates):
    if not raw_exdates:
        return set()
    return set(parse(dt) for dt in raw_exdates)

def fetch_event_overrides(cur, uid):
    cur.execute("""
                SELECT recurrence_id, new_start, new_end, new_summary
                FROM event_overrides
                WHERE event_uid = %s;
                """, (uid,))
    rows = cur.fetchall()
    # Mappe recurrence_id auf Override-Daten
    return {row[0]: {"new_start": row[1], "new_end": row[2], "new_summary": row[3]} for row in rows}

def generate_instances():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
                SELECT uid, dtstart, dtend, rrule, exdate, summary
                FROM events
                WHERE rrule IS NOT NULL;
                """)
    events = cur.fetchall()
    now = datetime.now()
    future_limit = now + timedelta(days=GENERATE_DAYS_AHEAD)

    for uid, dtstart, dtend, rrule_text, exdates, summary in events:
        print(f"🔁 Generiere Instanzen für Event {uid}...")

        # Alte Instanzen löschen
        cur.execute("DELETE FROM event_instances WHERE event_uid = %s;", (uid,))

        exdate_set = parse_exdates(exdates)
        overrides = fetch_event_overrides(cur, uid)

        rule = rrulestr(rrule_text, dtstart=dtstart)
        instances = rule.between(now, future_limit, inc=True)

        for start_time in instances:
            if start_time in exdate_set:
                print(f"⏭️  Ausgeschlossen: {start_time}")
                continue

            # Prüfe Override
            override = overrides.get(start_time)

            if override:
                inst_start = override["new_start"] or start_time
                inst_end = override["new_end"] or (inst_start + (dtend - dtstart if dtend else timedelta(hours=1)))
                inst_summary = override["new_summary"] or summary
                print(f"✏️  Override für {start_time}: Neuer Start {inst_start}")
            else:
                inst_start = start_time
                inst_end = start_time + (dtend - dtstart if dtend else timedelta(hours=1))
                inst_summary = summary

            # Instanz einfügen (hier nur start und end; summary könnte man in event_instances ergänzen)
            cur.execute("""
                        INSERT INTO event_instances (event_uid, instance_start, instance_end)
                        VALUES (%s, %s, %s);
                        """, (uid, inst_start, inst_end))

        conn.commit()

    cur.close()
    conn.close()
    print("✅ Instanzen inkl. Overrides erfolgreich generiert.")

if __name__ == "__main__":
    generate_instances()
