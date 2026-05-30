CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY,
    latitude NUMERIC(10, 7) NOT NULL,
    longitude NUMERIC(10, 7) NOT NULL,
    altitude NUMERIC(8, 2),
    country CHAR(2) NOT NULL DEFAULT 'PL',
    indoor BOOLEAN NOT NULL DEFAULT FALSE,
    exact_location BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sensors (
    id INTEGER PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    sensor_type VARCHAR(32) NOT NULL,
    manufacturer VARCHAR(64),
    pin VARCHAR(8),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sensors_location ON sensors(location_id);

CREATE TABLE IF NOT EXISTS measurements (
    id BIGINT PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    location_id INTEGER NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    measured_at TIMESTAMPTZ NOT NULL,
    pm10 NUMERIC(10, 2),
    pm25 NUMERIC(10, 2),
    pm1 NUMERIC(10, 2),
    temperature NUMERIC(6, 2),
    humidity NUMERIC(6, 2),
    pressure NUMERIC(10, 2),
    synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_measurements_sensor_time ON measurements(sensor_id, measured_at DESC);

CREATE TABLE IF NOT EXISTS sync_logs (
    id SERIAL PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    status VARCHAR(16) NOT NULL DEFAULT 'running',
    records_fetched INTEGER DEFAULT 0,
    records_saved INTEGER DEFAULT 0,
    error_message TEXT
);
