from psycopg2.errors import UndefinedTable

# Perform quality checks here
def data_quality_check(conn, table):
    """
    Function that check if table has rows

    Arguments:
    conn: <object> Posgres connection
    table: <list> list of tables from the schema

    returns None
    """
    # Get cursor from connection
    cur = conn.cursor()

    sql_test = """
        SELECT COUNT(*) 
        FROM {}
        LIMIT 10;
        """.format(table)
    try:
        cur.execute(sql_test)
        data_test = cur.fetchall()

        if len(data_test) < 1:
            raise ValueError("Table '{}' is empty".format(table))

        if data_test[0][0] < 1:
            raise ValueError("Table '{}' has no rows".format(table))

        print('Data Quality SUCCESS for table: {}. Total rows: {}'\
                .format(table, data_test[0][0]))


    except UndefinedTable as e:
        # Close Connection
        conn.close()
        raise Exception(e)