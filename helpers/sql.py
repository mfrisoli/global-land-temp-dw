# Create Tables
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
    );
"""

readings_by_city_create_table = """
    CREATE TABLE IF NOT EXISTS readings_by_city (
        by_city_id BIGINT IDENTITY(0,1),
        time_id NUMERIC,
        city_id NUMERIC,
        avg_temp NUMERIC,
        avf_temp_uncertainty NUMERIC,
        major_city BOOLEAN
    );
"""

time_create_table = """
    CREATE TABLE IF NOT EXISTS time (
        dt DATE,
        year SMALLINT,
        month SMALLINT,
        day SMALLINT,
        weekday SMALLINT,
        week SMALLINT
    );
"""

cities_create_table = """
    CREATE TABLE IF NOT EXISTS cities (
        city_id BIGINT IDENTITY(0,1),
        country_id NUMERIC,
        city TEXT,
        latitude TEXT,
        longitude TEXT
    );
"""

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
    CREDENTIALS 'aws_iam_role={}'
    REGION '{}'
    DELIMITER ','
    DATEFORMAT 'auto'
    IGNOREHEADER 1
    ;
"""
# Drop Tables

cities_table_drop = "DROP TABLE IF EXISTS cities;"

time_table_drop = "DROP TABLE IF EXISTS time;"

readings_by_city_table_drop = "DROP TABLE IF EXISTS readings_by_city;"

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"

sql_create_tables = [cities_create_table,
                     time_create_table,
                     readings_by_city_create_table,
                     staging_events_create_table
                    ]

sql_drop_tables = [cities_table_drop,
                   time_table_drop, 
                   readings_by_city_table_drop, 
                   staging_events_table_drop
                   ]
