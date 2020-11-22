from photo_queue import PhotoQueue
import sys
import db_setup
import api
from config import config
import process_photos as photos


def cleanup(cnx, cursor):
    cnx.commit()
    cursor.close()
    cnx.close()


def main():
    batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    conf = config
    (cnx, cursor) = db_setup.connect(**conf['db_config'])
    db_setup.create_tables(cursor=cursor)
    queue = PhotoQueue(cnx)
    queue.consume(
        process=photos.process(api.Api(conf['host']), cursor=cursor),
        batch_size=batch_size)
    cleanup(cnx=cnx, cursor=cursor)


if __name__ == "__main__":
    # find_unknown_faces_cmd()
    main()
    # lookup_faces_cmd()
