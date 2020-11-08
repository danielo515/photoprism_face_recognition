from db_setup.create_tables import create_tables
import sys
from datetime import datetime
import numpy as np
import face_recognition
import db_setup
import configparser
import api


def pic_from_queue(cursor, process, batch_size=5, skip=0):
    query = """
    select file_hash from photo_queue 
    where checked = False LIMIT %s OFFSET %s
    """
    cursor.execute(query, (batch_size, skip))
    time_start = datetime.now()
    for hash, in cursor:
        process(hash)
    print("Processed {} photos in queue in {} time".format(
        cursor.rowcount,
        datetime.now() - time_start)
    )

# =========== Face recognition section =============================


def print_result(filename, location):
    top, right, bottom, left = location
    print("{},{},{},{},{}".format(filename, top, right, bottom, left))


def find_faces(image_to_check, image_name, model, upsample):
    face_locations = face_recognition.face_locations(image_to_check, number_of_times_to_upsample=upsample, model=model)
    if len(face_locations) == 0:
        print(image_name, " has no faces")
    return face_locations


def process(api):
    def _process(hash):
        photo = api.fetch_photo(hash=hash)
        faces_found = find_faces(np.array(photo), image_name=hash, model="cnn", upsample=1)
        photo.save("output/0_{}_{}.jpg".format(len(faces_found), hash))
    return _process


if __name__ == "__main__":
    batch_size = int(sys.argv[1]) if sys.argv[1] else 5
    print(sys.argv[1])
    config = configparser.ConfigParser()
    config.read('./config.ini')
    db_config = dict(config['db_config'].items())
    photoprism_config = dict(config['photoprism'].items())
    host = photoprism_config.pop('host')

    (cnx, cursor) = db_setup.connect(**db_config)
    db_setup.create_tables(cursor=cursor)
    pic_from_queue(
        cursor=cursor,
        process=process(api.Api(host)),
        batch_size=batch_size, skip=50)

    cursor.close()
    cnx.close()
