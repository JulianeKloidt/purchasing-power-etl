CREATE TABLE countries (
    country_code VARCHAR(3) PRIMARY KEY,
    country_name TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    region TEXT,
    currency_code VARCHAR(3)
);

CREATE TABLE indicators (
    indicator_code TEXT PRIMARY KEY,
    indicator_name TEXT NOT NULL
);

CREATE TABLE indicator_values (
    country_code VARCHAR(3) NOT NULL,
    indicator_code TEXT NOT NULL,
    year INTEGER NOT NULL,
    value DOUBLE PRECISION,

    PRIMARY KEY (
        country_code,
        indicator_code,
        year
    ),

    FOREIGN KEY (country_code)
        REFERENCES countries(country_code),

    FOREIGN KEY (indicator_code)
        REFERENCES indicators(indicator_code)
);