# Drop Tables
cities_table_drop = "DROP TABLE IF EXISTS cities;"

time_table_drop = "DROP TABLE IF EXISTS time;"

readings_by_city_table_drop = "DROP TABLE IF EXISTS readings_by_city;"

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"

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
        date NUMERIC,
        city_id NUMERIC,
        avg_temp NUMERIC,
        avg_temp_uncertainty NUMERIC,
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
        country TEXT,
        city TEXT,
        latitude TEXT,
        longitude TEXT,
        major_city BOOLEAN
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

time_insert_table = """
    INSERT INTO time (
        dt,
        year,
        month,
        day,
        weekday,
        week)
    SELECT DISTINCT dt,
           EXTRACT (YEAR FROM dt) AS year,
           EXTRACT (MONTH FROM dt) AS month,
           EXTRACT (DAY FROM dt) AS day,
           EXTRACT (DOW FROM dt) AS weekday,
           EXTRACT (WEEK FROM dt) AS week
    FROM staging_events
    WHERE dt IS NOT NULL
    AND dt NOT IN (SELECT DISTINCT dt FROM time)
    ;
"""

cities_insert_table = """
    INSERT INTO cities (
        country,
        city,
        latitude,
        longitude,
        major_city
        )
    SELECT DISTINCT country,
        city,
        latitude,
        longitude,
        major_city
    FROM staging_events
    WHERE city IS NOT NULL
    AND city NOT IN (SELECT DISTINCT city FROM cities)
    ;
"""
readings_by_city_insert_table = """
    INSERT INTO readings_by_city (
        date,
        city_id,
        avg_temp,
        avg_temp_uncertainty,
    )
    SELECT DISTINCT se.dt AS date,
        c.city_id,
        se.AverageTemperature,
        se.AverageTemperatureUncertainty
    FROM staging_events se
    JOIN cities c 
        ON se.city=c.city
        AND se.country=c.country
        ;
"""


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

sql_insert_tables = [cities_insert_table, 
                     time_insert_table, 
                     readings_by_city_insert_table
                    ]
                    