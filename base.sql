CREATE TABLE events -- Organizer ist der Besitzer des Kalenders zu dem der Termin gehört
(
    id            SERIAL PRIMARY KEY,                           -- interne ID
    uid           VARCHAR(255) NOT NULL UNIQUE,                 -- iCalendar UID (CalDAV-Referenz)
    dtstamp       TIMESTAMP    NOT NULL,                        -- Erstell-/Änderungszeitpunkt
    dtstart       TIMESTAMP    NOT NULL,                        -- Startzeitpunkt
    dtend         TIMESTAMP,                                    -- Endzeitpunkt (optional, alternativ duration)
    duration      INTERVAL,                                     -- Dauer, wenn dtend nicht angegeben ist
    summary       TEXT,                                         -- Titel
    description   TEXT,                                         -- Beschreibung
    location      TEXT,                                         -- Ort
    status        ENUM ('TENTATIVE', 'CONFIRMED', 'CANCELLED'), -- Status: TENTATIVE, CONFIRMED, CANCELLED
    class         ENUM ('PUBLIC', 'PRIVATE', 'CONFIDENTIAL'),   -- Privatsphäre: PUBLIC, PRIVATE, CONFIDENTIAL
    transp        ENUM ('TRANSPARENT', 'OPAQUE'),               -- TRANSPARENT oder OPAQUE
    categories    TEXT[],                                       -- Kategorien als Array (z. B. PostgreSQL)
    rrule         TEXT,                                         -- Wiederholungsregel im iCalendar-Format
    exdate        TIMESTAMP[],                                  -- Ausnahmedaten (als iCalendar-Daten, z. B. 20250701T090000Z)
    recurrence_id TIMESTAMP,                                    -- Für Instanzen von wiederkehrenden Events
    sequence      INTEGER   DEFAULT 0,                          -- Versionsnummer
    last_modified TIMESTAMP,                                    -- Letzte Änderung
    created       TIMESTAMP DEFAULT NOW(),                      -- Erstellungszeitpunkt
    url           TEXT,                                         -- Optionale URL
    attach        TEXT[],                                       -- Liste von Anhängen (URLs oder Pfade)
    calendar      INT NOT NULL REFERENCES calendar(id) ON DELETE CASCADE,
);

CREATE TABLE event_instances
(
    id             SERIAL PRIMARY KEY,
    event_uid      VARCHAR(255) NOT NULL REFERENCES events (uid) ON DELETE CASCADE,
    instance_start TIMESTAMP    NOT NULL,
    instance_end   TIMESTAMP
);

CREATE TABLE event_overrides
(
    id            SERIAL PRIMARY KEY,
    event_uid     VARCHAR(255) NOT NULL REFERENCES events (uid) ON DELETE CASCADE,
    recurrence_id TIMESTAMP    NOT NULL, -- Welche Instanz wird überschrieben
    new_start     TIMESTAMP,             -- Optional neuer Start
    new_end       TIMESTAMP,             -- Optional neues Ende
    new_summary   TEXT                   -- Optional neuer Titel (kann man erweitern)
);

CREATE TABLE calendar
(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    owner INT NOT NULL REFERENCES user(id) ON DELETE CASCADE
)

CREATE TABLE calendar_share
(
    id SERIAL PRIMARY KEY,
    calendar_id INT NOT NULL REFERENCES calendar(id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    classification ENUM ('PUBLIC', 'PRIVATE', 'CONFIDENTIAL'),
    edit BOOLEAN NOT NULL DEFAULT true
)

CREATE TABLE attendees
(
    id        SERIAL PRIMARY KEY,
    event_instance_id INT NOT NULL REFERENCES event_instances(id) ON DELETE CASCADE,
    attendee  SERIAL       NOT NULL REFERENCES user (id) ON DELETE CASCADE,
    partstat  ENUM ('ACCEPTED', 'DECLINED', 'NEEDS-ACTION') DEFAULT 'NEEDS-ACTION',
    role      VARCHAR(20),
    rsvp      BOOLEAN DEFAULT FALSE
);

CREATE TABLE user
(
    id       SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email    VARCHAR(255) NOT NULL UNIQUE,
    created  TIMESTAMP DEFAULT NOW()
)

CREATE TABLE group
(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    owner INT NOT NULL REFERENCES user(id) ON DELETE CASCADE
)

CREATE TABLE group_members -- Wenn eine Gruppe zu einem Termin eingeladen wird, werden dadurch alle Mitglieder eingeladen
(
    id SERIAL PRIMARY KEY,
    group_id INT NOT NULL REFERENCES group(id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES user(id) ON DELETE CASCADE
)

CREATE TABLE contacts -- Man kann von allen Kontakten die öffentlichen Termine sehen
(
    id SERIAL PRIMARY KEY,
    user1 INT NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    user2 INT NOT NULL REFERENCES user(id) ON DELETE CASCADE
)