CREATE TYPE status AS ENUM ('TENTATIVE', 'CONFIRMED', 'CANCELLED');
CREATE TYPE classification AS ENUM ('PUBLIC', 'PRIVATE', 'CONFIDENTIAL');
CREATE TYPE transparent AS ENUM ('TRANSPARENT', 'OPAQUE');

CREATE TABLE events -- Organizer ist der Besitzer des Kalenders, zu dem der Termin gehört
(
    id            SERIAL PRIMARY KEY,                 -- interne ID
    uid           VARCHAR(255) NOT NULL UNIQUE,       -- iCalendar UID (CalDAV-Referenz)
    dtstamp       TIMESTAMP    NOT NULL,              -- Erstell-/Änderungszeitpunkt
    dtstart       TIMESTAMP    NOT NULL,              -- Startzeitpunkt
    dtend         TIMESTAMP,                          -- Endzeitpunkt (optional, alternativ duration)
    duration      INTERVAL,                           -- Dauer, wenn dtend nicht angegeben ist
    summary       TEXT,                               -- Titel
    description   TEXT,                               -- Beschreibung
    location      TEXT,                               -- Ort
    status        status         DEFAULT 'CONFIRMED', -- Status: TENTATIVE, CONFIRMED, CANCELLED
    class         classification DEFAULT 'PRIVATE',   -- Privatsphäre: PUBLIC, PRIVATE, CONFIDENTIAL
    transp        transparent    DEFAULT ('OPAQUE'),  -- TRANSPARENT oder OPAQUE
    categories    TEXT[],                             -- Kategorien als Array (z. B. PostgreSQL)
    rrule         TEXT,                               -- Wiederholungsregel im iCalendar-Format
    exdate        TIMESTAMP[],                        -- Ausnahmedaten (als iCalendar-Daten, z. B. 20250701T090000Z)
    recurrence_id TIMESTAMP,                          -- Für Instanzen von wiederkehrenden Events
    sequence      INTEGER        DEFAULT 0,           -- Versionsnummer
    last_modified TIMESTAMP      DEFAULT NOW(),       -- Letzte Änderung
    created       TIMESTAMP      DEFAULT NOW(),       -- Erstellungszeitpunkt
    url           TEXT,                               -- Optionale URL
    attach        TEXT[],                             -- Liste von Anhängen (URLs oder Pfade)
    calendar      INT          NOT NULL REFERENCES calendar (id) ON DELETE CASCADE
);

CREATE TABLE event_instances
(
    id             SERIAL PRIMARY KEY,
    event_uid      VARCHAR(255) NOT NULL REFERENCES events (uid) ON DELETE CASCADE,
    instance_start TIMESTAMP    NOT NULL,
    instance_end   TIMESTAMP
);

CREATE TABLE calendar
(
    id    SERIAL PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE,
    owner INT  NOT NULL REFERENCES user_account (id) ON DELETE CASCADE
);

CREATE TABLE calendar_share
(
    id             SERIAL PRIMARY KEY,
    calendar_id    INT     NOT NULL REFERENCES calendar (id) ON DELETE CASCADE,
    user_id        INT     NOT NULL REFERENCES user_account (id) ON DELETE CASCADE,
    classification classification   DEFAULT 'PRIVATE',
    edit           BOOLEAN NOT NULL DEFAULT true
);

CREATE TYPE participation_status AS ENUM ('ACCEPTED', 'DECLINED', 'NEEDS-ACTION');
CREATE TABLE attendees
(
    id                SERIAL PRIMARY KEY,
    event_instance_id INT NOT NULL REFERENCES event_instances (id) ON DELETE CASCADE,
    attendee          INT NOT NULL REFERENCES user_account (id) ON DELETE CASCADE,
    partstat          participation_status DEFAULT 'NEEDS-ACTION',
    role              VARCHAR(20),
    rsvp              BOOLEAN              DEFAULT FALSE
);

CREATE TABLE person
(
    id        SERIAL PRIMARY KEY,
    firstName VARCHAR(255) NOT NULL,
    lastName  VARCHAR(255),
    birthDate DATE
);

CREATE TABLE user_account
(
    username VARCHAR(255)    NOT NULL UNIQUE,
    password VARCHAR(255)    NOT NULL,
    email    VARCHAR(255)    NOT NULL UNIQUE,
    created  TIMESTAMP DEFAULT NOW(),
    id       INT PRIMARY KEY NOT NULL REFERENCES person (id) ON DELETE CASCADE
);

CREATE TABLE user_group
(
    id    SERIAL PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE,
    owner INT  NOT NULL REFERENCES user_account (id) ON DELETE CASCADE
);

CREATE TABLE group_members -- Wenn eine Gruppe zu einem Termin eingeladen wird, werden dadurch alle Mitglieder eingeladen
(
    id       SERIAL PRIMARY KEY,
    group_id INT NOT NULL REFERENCES user_group (id) ON DELETE CASCADE,
    user_id  INT NOT NULL REFERENCES user_account (id) ON DELETE CASCADE
);

CREATE TABLE contacts -- Man kann von allen Kontakten die öffentlichen Termine sehen
(
    id    SERIAL PRIMARY KEY,
    user1 INT NOT NULL REFERENCES user_account (id) ON DELETE CASCADE,
    user2 INT NOT NULL REFERENCES user_account (id) ON DELETE CASCADE
);

CREATE TABLE meal
(
    id    SERIAL PRIMARY KEY,
    name  TEXT,
    event INT NOT NULL REFERENCES event_instances (id) ON DELETE CASCADE
);

CREATE TABLE kitchen_chore
(
    id        SERIAL PRIMARY KEY,
    meal_id   INT NOT NULL REFERENCES meal (id) ON DELETE CASCADE,
    person_id INT NOT NULL REFERENCES person (id) ON DELETE CASCADE
);

CREATE TABLE toilet_chore
(
    id        SERIAL PRIMARY KEY,
    event     INT NOT NULL REFERENCES event_instances (id) ON DELETE CASCADE,
    person_id INT NOT NULL REFERENCES person (id) ON DELETE CASCADE
);

CREATE TABLE chore
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    dtstart     DATE,
    dtend       DATE,
    project_id  INT          NOT NULL REFERENCES project (id) ON DELETE CASCADE
);

CREATE TABLE chore_responsibility
(
    id       SERIAL PRIMARY KEY,
    chore_id INT NOT NULL REFERENCES chore (id) ON DELETE CASCADE,
    user_id  INT NOT NULL REFERENCES user_account (id) ON DELETE CASCADE
);

CREATE TABLE task
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    done        BOOLEAN      NOT NULL DEFAULT FALSE,
    deadline    DATE,
    project_id  INT          NOT NULL REFERENCES project (id) ON DELETE CASCADE,
    description TEXT
);

CREATE TABLE task_responsibility
(
    id      SERIAL PRIMARY KEY,
    task_id INT NOT NULL REFERENCES task (id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES user_account (id) ON DELETE CASCADE
);

CREATE TABLE meeting
(
    id       SERIAL PRIMARY KEY,
    protocol TEXT,
    agenda   TEXT
);

CREATE TABLE project
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    calendar_id INT          NOT NULL REFERENCES calendar (id) ON DELETE RESTRICT, -- Der Kalender für alles auf der Freizeit (Mahlzeiten, Programmpunkte)
    house_url   VARCHAR(255),
    event_id    INT          NOT NULL REFERENCES event_instances (id) ON DELETE RESTRICT
);

CREATE TABLE project_participant
(
    id         SERIAL PRIMARY KEY,
    project_id INT NOT NULL REFERENCES project (id) ON DELETE CASCADE,
    person_id  INT NOT NULL REFERENCES person (id) ON DELETE CASCADE
);

CREATE TABLE project_team
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    calendar_id INT          NOT NULL REFERENCES calendar (id) ON DELETE RESTRICT -- Der Kalender wird für Vortreffen usw benutzt
);

CREATE TABLE project_team_member
(
    id              SERIAL PRIMARY KEY,
    project_team_id INT NOT NULL REFERENCES project_team (id) ON DELETE CASCADE,
    user_id         INT NOT NULL REFERENCES user_account (id) ON DELETE CASCADE
);

CREATE OR REPLACE VIEW event_instance_overview AS
SELECT events.*,
       event_instances.*,
       calendar.name                                                          AS calendar_name,

       COUNT(attendees.id) FILTER (WHERE attendees.partstat = 'ACCEPTED')     AS accepted_count,
       COUNT(attendees.id) FILTER (WHERE attendees.partstat = 'DECLINED')     AS declined_count,
       COUNT(attendees.id) FILTER (WHERE attendees.partstat = 'NEEDS-ACTION') AS needs_action_count

FROM events
         JOIN event_instances ON event_instances.event_uid = events.uid
         JOIN calendar ON events.calendar = calendar.id
         LEFT JOIN calendar_share ON calendar_share.calendar_id = calendar.id
         LEFT JOIN attendees ON attendees.event_instance_id = event_instances.id

GROUP BY events.id, event_instances.id, calendar.name;