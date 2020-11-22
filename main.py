from photo_queue import PhotoQueue
from re import template
from face_recognition.api import face_encodings, face_locations
from db_setup.create_tables import create_tables
import sys
import db_setup
import api
from config import config
import faces


def flag_photo_as_processed(file_id, cursor, face_count=0):
    # print("Flagging", file_id)
    cursor.execute("""
    UPDATE photo_queue
    SET checked = 1, face_count = %s
    WHERE file_id = %s;
    """, (face_count, file_id))


def process(api, cursor):
    def _process(hash, file_id):
        photo = api.fetch_photo(hash=hash)
        if photo == None:
            print('Skipped photo {}'.format(file_id))
            return flag_photo_as_processed(file_id=file_id, cursor=cursor)

        (encodings, locations) = faces.find_in_photo(photo)
        if(len(encodings) > 0):
            faces.save_to_db(
                image_id=file_id, cursor=cursor,
                encodings=encodings, locations=locations,
            )
            photo.save("output/{}_{}.jpg".format(len(locations), hash))
        flag_photo_as_processed(
            file_id=file_id, cursor=cursor, face_count=len(locations)
        )
    return _process


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
        process=process(api.Api(conf['host']), cursor=cursor),
        batch_size=batch_size)
    cleanup(cnx=cnx, cursor=cursor)


if __name__ == "__main__":
    # find_unknown_faces_cmd()
    main()
    # lookup_faces_cmd()
