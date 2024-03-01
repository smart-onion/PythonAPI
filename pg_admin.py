import os
import dotenv
import psycopg2

dotenv.load_dotenv()


def connect_db(func):
    """
    Decorator function for connecting to the PostgreSQL database.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapped function with database connection and cursor handling.
    """
    def wrapper(*args, **kwargs):
        # Database connection parameters
        db_params = {
            'host': os.environ.get('DB_HOST'),
            'database': os.environ.get('DB_NAME'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'port': os.environ.get('DB_PORT')
        }

        # Establish a connection
        pg_conn = psycopg2.connect(**db_params)

        # Create a cursor from the connection
        pg_cursor = pg_conn.cursor()

        # Function call with cursor
        result = func(pg_cursor, *args, **kwargs)

        # Commit changes to the database
        pg_conn.commit()

        # Close the cursor and connection
        pg_cursor.close()
        pg_conn.close()

        return result

    return wrapper


@connect_db
def get_folio_id(pg_cursor, username: str):
    """
    Retrieves the folio ID of a given username from the database.

    Args:
        pg_cursor (psycopg2.cursor): The PostgreSQL cursor.
        username (str): The username to search for.

    Returns:
        str: The folio ID if found, "NOT_FOUND" otherwise.
    """
    assert type(username) is str

    # Example query
    pg_query = f"SELECT folio_id FROM guests WHERE guest='{username}'"

    pg_cursor.execute(pg_query)
    result = pg_cursor.fetchall()

    try:
        return result[0][0]
    except Exception as ex:
        print(ex)
        return "NOT_FOUND"


@connect_db
def insert_pass_logs(pg_cursor, user: str, username: str, hostname: str):
    """
    Inserts password change logs into the database.

    Args:
        pg_cursor (psycopg2.cursor): The PostgreSQL cursor.
        user (str): The user performing the password change.
        username (str): The username whose password is changed.
        hostname (str): The hostname where the password change occurs.

    Returns:
        str: "DONE" if successful, "NOT_FOUND" otherwise.
    """
    assert type(user) is str
    assert type(username) is str
    assert type(hostname) is str

    id_query = f"select id from guests where guest='{username}'"
    pg_cursor.execute(id_query)
    id = pg_cursor.fetchall()
    if id:
        set_query = f"INSERT INTO change_pass_logs (username, guest_id, hostname) VALUES ('{user}', {id[0][0]}, '{hostname}')"
        pg_cursor.execute(set_query)
        print(":db")
        return 'DONE'
    else:
        return 'NOT_FOUND'


@connect_db
def get_pass_logs(pg_cursor):
    """
    Retrieves password change logs from the database.

    Args:
        pg_cursor (psycopg2.cursor): The PostgreSQL cursor.

    Returns:
        list: A list of tuples containing password change logs.
    """
    get_query = ("SELECT username, time, guest, folio_id, f_name, l_name FROM change_pass_logs JOIN guests ON "
                 "guests.id=change_pass_logs.guest_id ORDER BY time DESC LIMIT 10")
    pg_cursor.execute(get_query)
    result = pg_cursor.fetchall()
    return result


@connect_db
def is_authenticated(pg_cursor, username: str, password: str):
    """
    Checks if a user is authenticated by verifying the username and password.

    Args:
        pg_cursor (psycopg2.cursor): The PostgreSQL cursor.
        username (str): The username to authenticate.
        password (str): The password to authenticate.

    Returns:
        bool: True if authenticated, False otherwise.
    """
    assert type(username) is str
    assert type(password) is str

    query = f"SELECT password FROM users WHERE username='{username}'"
    pg_cursor.execute(query)
    result = pg_cursor.fetchall()

    try:
        if result[0][0] == password:
            return True
        else:
            return False
    except Exception:
        return False
