from jinja2 import Template
from PIL import Image, ImageDraw
import json
from face_recognition.api import face_encodings, face_locations
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
        print(cursor.rowcount)
        cnx.commit()
    print("Processed {} photos in queue in {} time".format(
        count,
        datetime.now() - time_start)
    )

# =========== Face recognition section =============================


encoding_columns = ["TERM_{} ".format(i) for i in range(128)]

save_query = Template("""
INSERT INTO faces 
(photo_id, locations, {{ encoding_columns | join(',') }})
VALUES (%s, %s, {% for i in range(127) %} %s, {% endfor %} %s)
""").render(encoding_columns=encoding_columns)


def save_faces(image_id, encodings, locations, cursor):
    for (encoding, location) in zip(encodings, locations):
        cursor.execute(save_query, (image_id, json.dumps(location)) + tuple(encoding))


def flag_photo_as_processed(photo_id, cursor, face_count=0):
    # print("Flagging", photo_id)
    cursor.execute("""
    UPDATE photo_queue
    SET checked = 1, face_count = %s
    WHERE photo_id = %s;
    """, (face_count, photo_id))


def get_encodings(image, faces_locations):
    return [face_recognition.face_encodings(
            image,
            known_face_locations=locations)
            for locations in faces_locations]


def find_faces(image_to_check, image_name, model, upsample):
    face_locations = face_recognition.face_locations(image_to_check, number_of_times_to_upsample=upsample, model=model)
    # if len(face_locations) > 0:
    #     print(image_name, " has {} faces".format(len(face_locations)))
    return face_locations


def process(api, cursor):
    def _process(hash, photo_id):
        photo = api.fetch_photo(hash=hash)
        if photo == None:
            print('Skipped photo {}'.format(photo_id))
            flag_photo_as_processed(photo_id=photo_id, cursor=cursor)
            return

        photo_arr = np.array(photo)
        faces_found = find_faces(
            photo_arr,
            image_name=hash,
            model="cnn",
            upsample=0)
        if(len(faces_found) > 0):
            faces_encodings = face_recognition.face_encodings(photo_arr, known_face_locations=faces_found)
            save_faces(
                image_id=photo_id, cursor=cursor,
                encodings=faces_encodings, locations=faces_found,
            )
            photo.save("output/{}_{}.jpg".format(len(faces_found), hash))
        flag_photo_as_processed(photo_id=photo_id, cursor=cursor, face_count=len(faces_found))
    return _process


def find_closest_match_by_id(*, face_id, cursor):
    template = Template(open('./queries/get_face_encodings.sql.jinja').read())
    query = template.render()
    cursor.execute(query, (face_id,))
    encodings = cursor.fetchall()[0]
    return find_closest_match_in_db(face_encodings=encodings, cursor=cursor)


def find_closest_match_in_db(*, face_encodings, cursor):
    template = Template(open('./queries/find_closest_match.sql.jinja').read())
    query = template.render(encodings=enumerate(face_encodings))
    cursor.execute(query)
    return cursor.fetchall()


def show_prediction_labels_on_image(img, predictions):
    """
    Shows the face recognition results visually.

    :param img an already loaded image 
    :param predictions: array of label, positions tuples
    :return:
    """
    pil_image = img.convert("RGB")
    draw = ImageDraw.Draw(pil_image)

    for confidence, (top, right, bottom, left) in predictions:
        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # There's a bug in Pillow where it blows up with non-UTF-8 text
        # when using the default bitmap font
        confidence = confidence.encode("UTF-8")

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(confidence)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), confidence, fill=(255, 255, 255, 255))

    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Display the resulting image
    pil_image.show()


def read_config():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    db_config = dict(config['db_config'].items())
    photoprism_config = dict(config['photoprism'].items())
    host = photoprism_config.pop('host')

    return dict(
        host=host,
        photoprism_config=photoprism_config,
        db_config=db_config
    )


def main():
    batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    conf = read_config()
    (cnx, cursor) = db_setup.connect(**conf['db_config'])
    db_setup.create_tables(cursor=cursor)
    pic_from_queue(
        cnx=cnx,
        process=process(api.Api(conf['host']), cursor=cursor),
        batch_size=batch_size, skip=50)
    cnx.commit()
    cursor.close()
    cnx.close()


def lookup_faces_cmd():
    if (len(sys.argv) < 2):
        print('Please provide a face id')
        exit(1)
    face_id = int(sys.argv[1])
    conf = read_config()
    (cnx, cursor) = db_setup.connect(**conf['db_config'])
    results = find_closest_match_by_id(face_id=face_id, cursor=cursor)
    _api = api.Api(conf['host'])
    print("Found {} faces".format(len(results)))
    images = [
        (_api.get_img_url(hash=hash), json.loads(locations))
        for (_, locations, hash, confidence) in results
    ]
    with open('results.html', 'w') as f:
        rendered = Template(open('./templates/faces.jinja.html').read()).render(images=images)
        f.write(rendered)


if __name__ == "__main__":
    # main()
    lookup_faces_cmd()
