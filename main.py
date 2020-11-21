from photo_queue import PhotoQueue
from re import template
from jinja2 import FileSystemLoader, Environment
import json
from face_recognition.api import face_encodings, face_locations
from db_setup.create_tables import create_tables
import sys
import db_setup
import api
import os
import webbrowser
from config import config
import faces


# =========== Face recognition section =============================


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


def render_html(*, template_name, output, **args):
    str = open(template_name).read()
    template = Environment(loader=FileSystemLoader(os.path.realpath('./server/templates'))).from_string(str)
    rendered = template.render(args)
    with open(output, 'w') as f:
        f.write(rendered)


def find_unknown_faces_cmd():
    (cnx, cursor) = db_setup.connect(**config['db_config'])
    images = faces.find_unknown_in_db(cursor=cursor, api=api.Api(config['host']))
    render_html(
        output='output/unknown.html', template_name='./templates/unknown_faces.html.jinja', images=images, crop_size=100)
    webbrowser.open('file://{}'.format(os.path.realpath('./unknown.html')))
    cleanup(cnx=cnx, cursor=cursor)


def lookup_faces_cmd():
    if (len(sys.argv) < 2):
        print('Please provide a face id')
        exit(1)
    face_id = int(sys.argv[1])
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    (cnx, cursor) = db_setup.connect(**config['db_config'])
    results = faces.find_closest_match_by_id(face_id=face_id, cursor=cursor, limit=limit)
    _api = api.Api(config['host'])
    print("Found {} faces".format(len(results)))
    images = [
        (_api.get_img_url(hash=hash), json.loads(locations), distance, id)
        for (id, locations, hash, distance) in results
    ]
    render_html(
        output='output/results.html', template_name='./templates/faces.jinja.html',
        images=images)
    webbrowser.open('file://{}'.format(os.path.realpath('./results.html')))
    cleanup(cnx=cnx, cursor=cursor)


if __name__ == "__main__":
    # find_unknown_faces_cmd()
    main()
    # lookup_faces_cmd()
