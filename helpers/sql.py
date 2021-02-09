staging_events_create_table = """
    CREATE TABLE IF NOT EXISTS staging_events (
        index NUMERIC,
        dt DATE NOT NULL,
        AverageTemperature NUMERIC,
        AverageTemperatureUncertainty NUMERIC,
        City TEXT,
        Country TEXT,
        Latitude TEXT,
        Longitude TEXT,
        major_city BOOLEAN
    )
"""

# Fact Tables BIGINT IDENTITY(0,1)

readings_by_city_create_table = """
    CREATE TABLE IF NOT EXISTS readings_by_city (
        by_city_id SERIAL,
        time_id NUMERIC,
        city_id NUMERIC,
        avg_temp NUMERIC,
        avf_temp_uncertainty NUMERIC,
        major_city BOOLEAN
    )
"""

# Dimension tables

time_create_table = """
    CREATE TABLE IF NOT EXISTS time (
        dt DATE,
        year SMALLINT,
        month SMALLINT,
        day SMALLINT,
        weekday SMALLINT,
        week SMALLINT
    )
"""

cities_create_table = """
    CREATE TABLE IF NOT EXISTS cities (
        city_id SERIAL,
        country_id NUMERIC,
        city TEXT,
        latitude TEXT,
        longitude TEXT
    )
"""

sql_create_tables = [cities_create_table,
                     time_create_table,
                     readings_by_city_create_table,
                     staging_events_create_table
                    ]

# Insert SQL statements

staging_insert = """
    COPY staging_events (
        index,
        dt,
        AverageTemperature,
        AverageTemperatureUncertainty,
        City,
        Country,
        Latitude,
        Longitude,
        major_city
    )
    FROM  '{}'
    DELIMITER ','
    CSV HEADER
"""