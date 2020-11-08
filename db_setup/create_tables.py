
import mysql.connector
from mysql.connector import errorcode


def create_faces_table():
    rows = [" TERM_{} DOUBLE".format(n) for n in range(128)]
    query = '''
        create table if not exists faces (
            id bigint auto_increment primary key,
            photo_id int(10) unsigned not null,
            locations JSON not null,
            {rows},
            FOREIGN KEY fk (photo_id) REFERENCES photos (id) ON UPDATE RESTRICT
        ) ENGINE = InnoDB;
    '''.format(rows=",\n".join(rows))
    return query


def create_photo_queue_table():
    query = '''
    create table if not exists photo_queue (
        checked boolean default false
        ) ENGINE = InnoDB SELECT photo_id, file_hash from files;
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
        return (cnx, cnx.cursor())


def create_tables(cursor):
    create_table(name='faces', description=create_faces_table(), cursor=cursor)
    create_table(name='photo_queue', description=create_photo_queue_table(), cursor=cursor)
