def execute_sql(sql, connection, fetch=True):
    """executes the sql code using the connection provided.

    Parameters
    __________
    sql : str
        sql code to executed
    connection : psycopg2 connection object
    fetch : bool
        True if query should return results


    Returns
    _______
         results of sql execution. A psycopg2 results object or None

    """
    print(f"about to execute: {sql}")
    results = None
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            if fetch:
                results = cursor.fetchall()
    connection.close()
    return results
