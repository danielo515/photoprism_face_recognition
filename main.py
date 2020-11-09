from jinja2 import Template
import json
from face_recognition.api import face_locations
from db_setup.create_tables import create_tables
import sys
from datetime import datetime
import numpy as np
import face_recognition
import db_setup
import configparser
import api


def pic_from_queue(cnx, process, batch_size=5, skip=0):
    cursor = cnx.cursor()
    countQuery = "SELECT count(photo_id) FROM photo_queue WHERE checked = FALSE"
    cursor.execute(countQuery)
    (count,) = cursor.fetchall()[0]
    print("There are {} items on the queue".format(count))
    query = """
    SELECT photo_id, file_hash FROM photo_queue 
    WHERE checked = False LIMIT %s OFFSET %s
    """
    time_start = datetime.now()
    for batch in range(int(count/batch_size)):
        cursor.execute(query, (batch_size, skip))
        for (photo_id, hash) in cursor.fetchall():
            # try:
            process(hash=hash, photo_id=photo_id)
            # except:
            #     print("An error ocurred in batch {} processing {}".format(batch, photo_id))
        cnx.commit()
    print("Processed {} photos in queue in {} time".format(
        count,
        datetime.now() - time_start)
    )

# =========== Face recognition section =============================


def print_result(filename, location):
    top, right, bottom, left = location
    print("{},{},{},{},{}".format(filename, top, right, bottom, left))


encoding_columns = ["TERM_{} ".format(i) for i in range(128)]

save_query = Template("""
INSERT INTO faces 
(photo_id, locations, {{ encoding_columns | join(',') }})
VALUES (%s, %s, {% for i in range(127) %} %s, {% endfor %} %s)
""").render(encoding_columns=encoding_columns)


def save_faces(image_id, encodings, locations, cursor):
    for (encoding, location) in zip(encodings, locations):
        cursor.execute(save_query, (image_id, json.dumps(location)) + tuple(encoding))


def flag_photo_as_processed(photo_id, cursor):
    # print("Flagging", photo_id)
    cursor.execute("""
    UPDATE photo_queue
    SET checked = 1
    WHERE photo_id = %s;
    """, (photo_id, ))


def get_encodings(image, faces_locations):
    return [face_recognition.face_encodings(
            image,
            known_face_locations=locations)
            for locations in faces_locations]


def find_faces(image_to_check, image_name, model, upsample):
    face_locations = face_recognition.face_locations(image_to_check, number_of_times_to_upsample=upsample, model=model)
    if len(face_locations) > 0:
        print(image_name, " has {} faces".format(len(face_locations)))
    return face_locations


def process(api, cursor):
    def _process(hash, photo_id):
        photo = api.fetch_photo(hash=hash)
        if photo != None:
            photo_arr = np.array(photo)
            faces_found = find_faces(
                photo_arr,
                image_name=hash,
                model="cnn",
                upsample=1)
            if(len(faces_found) > 0):
                faces_encodings = face_recognition.face_encodings(
                    photo_arr, known_face_locations=faces_found
                )
                save_faces(
                    image_id=photo_id, encodings=faces_encodings, locations=faces_found,
                    cursor=cursor
                )
                photo.save("output/0_{}_{}.jpg".format(len(faces_found), hash))
        else:
            print('Skipped photo {}'.format(photo_id))
        flag_photo_as_processed(photo_id=photo_id, cursor=cursor)
    return _process


if __name__ == "__main__":
    batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    config = configparser.ConfigParser()
    config.read('./config.ini')
    db_config = dict(config['db_config'].items())
    photoprism_config = dict(config['photoprism'].items())
    host = photoprism_config.pop('host')

    (cnx, cursor) = db_setup.connect(**db_config)
    db_setup.create_tables(cursor=cursor)
    pic_from_queue(
        cnx=cnx,
        process=process(api.Api(host), cursor=cursor),
        batch_size=batch_size, skip=50)
    cnx.commit()
    cursor.close()
    cnx.close()
