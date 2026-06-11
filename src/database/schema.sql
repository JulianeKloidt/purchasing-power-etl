CREATE TABLE IF NOT EXISTS indicator_values (
    id SERIAL PRIMARY KEY,

    country_code VARCHAR(3) NOT NULL,
    indicator_code VARCHAR(30) NOT NULL,

    year INT NOT NULL,
    value DOUBLE PRECISION,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE indicator_values
ADD CONSTRAINT unique_indicator_observation
UNIQUE (country_code, indicator_code, year);

CREATE INDEX idx_indicator_lookup
ON indicator_values (country_code, indicator_code, year);