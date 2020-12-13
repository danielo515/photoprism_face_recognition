
import mysql.connector
from mysql.connector import errorcode

tables = {
    'people': """
        CREATE TABLE if NOT EXISTS people (
            id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            name TEXT NOT NULL
        ) ENGINE = InnoDB;
    """
}


def create_faces_table():
    rows = [" TERM_{} DOUBLE".format(n) for n in range(128)]
    query = '''
        CREATE TABLE if NOT EXISTS faces (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            file_id INT(10) UNSIGNED NOT NULL,
            person_id INT(10) UNSIGNED NULL,
            locations JSON NOT NULL,
            {rows},
            FOREIGN KEY fk (file_id) REFERENCES files (id),
            FOREIGN KEY person_fk (person_id) REFERENCES people (id) ON DELETE SET NULL
        ) ENGINE = InnoDB;
    '''.format(rows=",\n".join(rows))
    return query


def create_photo_queue_table():
    "File type is BINARY that is the representation of JPEG"
    query = '''
    create table if not exists photo_queue (
        checked boolean default false,
        face_count INT UNSIGNED DEFAULT 0 NOT NULL
        ) ENGINE = InnoDB 
        SELECT id as file_id, file_hash from files
        WHERE file_type IN (0x6A7067)
        '''
    return query


def create_table(name, description, cursor):
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
            print(description)
    else:
        print("OK")


def connect(*, user, password, host):
    try:
        cnx = mysql.connector.connect(user=user, password=password, host=host, database='photoprism', raise_on_warnings=True)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return (cnx, cnx.cursor(buffered=True))


def create_tables(cursor):
    create_table(name='people', description=tables['people'], cursor=cursor)
    create_table(name='faces', description=create_faces_table(), cursor=cursor)
    create_table(name='photo_queue', description=create_photo_queue_table(), cursor=cursor)
