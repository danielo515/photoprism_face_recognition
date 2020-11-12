from re import template
from jinja2 import Template, FileSystemLoader, Environment
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
import os
import webbrowser
from queries import Queries


def pic_from_queue(cnx, process, batch_size=5, skip=0):
    cursor = cnx.cursor()
    countQuery = "SELECT count(file_id) FROM photo_queue WHERE checked = FALSE"
    cursor.execute(countQuery)
    (count,) = cursor.fetchall()[0]
    print("There are {} items on the queue".format(count))
    query = """
    SELECT file_id, file_hash FROM photo_queue 
    WHERE checked = False LIMIT %s OFFSET %s
    """
    time_start = datetime.now()
    for batch in range(int(count/batch_size)):
        cursor.execute(query, (batch_size, skip))
        for (file_id, hash) in cursor.fetchall():
            # try:
            process(hash=hash, file_id=file_id)
            # except:
            #     print("An error ocurred in batch {} processing {}".format(batch, file_id))
        print(cursor.rowcount)
        cnx.commit()
    print("Processed {} photos in queue in {} time".format(
        count,
        datetime.now() - time_start)
    )

# =========== Face recognition section =============================


def save_faces(image_id, encodings, locations, cursor):
    for (encoding, location) in zip(encodings, locations):
        cursor.execute(
            Queries.save_face,
            (image_id, json.dumps(location)) + tuple(encoding))


def flag_photo_as_processed(file_id, cursor, face_count=0):
    # print("Flagging", file_id)
    cursor.execute("""
    UPDATE photo_queue
    SET checked = 1, face_count = %s
    WHERE file_id = %s;
    """, (face_count, file_id))


def get_encodings(image, faces_locations):
    return [face_recognition.face_encodings(
            image,
            known_face_locations=locations)
            for locations in faces_locations]


def find_faces(image_to_check, model, upsample):
    face_locations = face_recognition.face_locations(image_to_check, number_of_times_to_upsample=upsample, model=model)
    return face_locations


def process(api, cursor):
    def _process(hash, file_id):
        photo = api.fetch_photo(hash=hash)
        if photo == None:
            print('Skipped photo {}'.format(file_id))
            flag_photo_as_processed(file_id=file_id, cursor=cursor)
            return

        photo_arr = np.array(photo)
        faces_found = find_faces(
            photo_arr,
            model="cnn",
            upsample=0)
        if(len(faces_found) > 0):
            faces_encodings = face_recognition.face_encodings(photo_arr, known_face_locations=faces_found)
            save_faces(
                image_id=file_id, cursor=cursor,
                encodings=faces_encodings, locations=faces_found,
            )
            photo.save("output/{}_{}.jpg".format(len(faces_found), hash))
        flag_photo_as_processed(file_id=file_id, cursor=cursor, face_count=len(faces_found))
    return _process


def find_closest_match_by_id(*, face_id, cursor, limit=50):
    query = Queries.get_face_encodings.render()
    cursor.execute(query, (face_id,))
    encodings = cursor.fetchall()[0]
    return find_closest_match_in_db(face_encodings=encodings, cursor=cursor, limit=limit)


def find_closest_match_in_db(*, face_encodings, cursor, limit=50):
    query = Queries.find_closest_match.render(encodings=enumerate(face_encodings))
    cursor.execute(query, {'limit': limit})
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


def cleanup(cnx, cursor):
    cnx.commit()
    cursor.close()
    cnx.close()


def main():
    batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    conf = read_config()
    (cnx, cursor) = db_setup.connect(**conf['db_config'])
    db_setup.create_tables(cursor=cursor)
    pic_from_queue(
        cnx=cnx,
        process=process(api.Api(conf['host']), cursor=cursor),
        batch_size=batch_size, skip=50)
    cleanup(cnx=cnx, cursor=cursor)


def render_html(*, template_name, output, images):
    str = open(template_name).read()
    template = Environment(loader=FileSystemLoader(os.path.realpath('./templates'))).from_string(str)
    rendered = template.render(images=images)
    with open(output, 'w') as f:
        f.write(rendered)


def find_unknown_faces(*, cursor, api, limit=200):
    cursor.execute(Queries.unknown_faces.render(), {'limit': limit})
    results = []
    for (a_id, a_locations, a_hash, b_id, b_locations, b_hash, _) in cursor:
        results.append((api.get_img_url(hash=a_hash), json.loads(a_locations), a_id))
        results.append((api.get_img_url(hash=b_hash),  json.loads(b_locations), b_id))
    return results


def find_unknown_faces_cmd():
    conf = read_config()
    (cnx, cursor) = db_setup.connect(**conf['db_config'])
    _api = api.Api(conf['host'])
    images = find_unknown_faces(cursor=cursor, api=_api)
    render_html(
        output='unknown.html', template_name='./templates/unknown_faces.html.jinja', images=images)
    webbrowser.open('file://{}'.format(os.path.realpath('./unknown.html')))
    cleanup(cnx=cnx, cursor=cursor)


def lookup_faces_cmd():
    if (len(sys.argv) < 2):
        print('Please provide a face id')
        exit(1)
    face_id = int(sys.argv[1])
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    conf = read_config()
    (cnx, cursor) = db_setup.connect(**conf['db_config'])
    results = find_closest_match_by_id(face_id=face_id, cursor=cursor, limit=limit)
    _api = api.Api(conf['host'])
    print("Found {} faces".format(len(results)))
    images = [
        (_api.get_img_url(hash=hash), json.loads(locations), distance, id)
        for (id, locations, hash, distance) in results
    ]
    render_html(
        output='results.html', template_name='./templates/faces.jinja.html',
        images=images, )
    webbrowser.open('file://{}'.format(os.path.realpath('./results.html')))
    cleanup(cnx=cnx, cursor=cursor)


if __name__ == "__main__":
    find_unknown_faces_cmd()
    # main()
    # lookup_faces_cmd()
