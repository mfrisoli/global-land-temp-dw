from psycopg2.errors import UndefinedTable
import psycopg2

# Perform quality checks here
def data_quality_check(conn, table):
    """
    Function that check if table is not empty and has rows

    Arguments:
    conn: <object> Posgres connection
    table: str table name from the schema

    returns None
    """
    # Get cursor from connection
    cur = conn.cursor()
    
    sql_test_data = """
        SELECT *
        FROM {}
        LIMIT 10;
        """.format(table)

    sql_test_count = """
        SELECT COUNT(*) 
        FROM {};
        """.format(table)
    try:
        cur.execute(sql_test_count)
        data_test_count = cur.fetchall()

        cur.execute(sql_test_data)
        data_test_data = cur.fetchall()

        if len(sql_test_data) < 1:
            raise ValueError("Table '{}' is empty".format(table))

        if data_test_count[0][0] < 1:
            raise ValueError("Table '{}' has no rows".format(table))    

        print('Data Quality SUCCESS for table: {}. Total rows: {}'\
                .format(table, data_test_count[0][0]))

    except UndefinedTable as e:
        # Close Connection
        conn.close()
        raise Exception(e)



def data_integrity_check(conn, table, column_data_types):
    """
    Function that check if table has rows

    Arguments:
    conn: <object> Posgres connection
    table: str table name from the schema
    column_data_types: list of coumn data types

    returns: None
    """
    # Get cursor from connection
    cur = conn.cursor()

    sql_test_integrity = """
        SELECT * 
        FROM {}
        LIMIT 10;
        """.format(table)

    try:
        cur.execute(sql_test_integrity)
        data_test_integrity = cur.fetchall()

        for col, col_type in zip(data_test_integrity[0],column_data_types):

            col_format = "<class '{}'>".format(col_type)

            if not (str(type(col)) == col_format):

                raise ValueError("Table '{}' with invalid data type, \
                    should be {} but instead got {}".format(table, col_format, type(col)))

        print('Data Integrity SUCCESS for table: {}'.format(table))

    except Exception as e:
        # Close Connection
        conn.close()
        raise Exception(e)