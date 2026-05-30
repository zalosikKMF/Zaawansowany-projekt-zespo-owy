-- ClearAir – schemat PostgreSQL (Sensor.Community)

CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY,
    latitude NUMERIC(10, 7) NOT NULL,
    longitude NUMERIC(10, 7) NOT NULL,
    altitude NUMERIC(8, 2),
    country CHAR(2) NOT NULL DEFAULT chr(39)+'PL'+chr(39),
    indoor BOOLEAN NOT NULL DEFAULT FALSE,
    exact_location BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
