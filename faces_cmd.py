
from db_setup.create_tables import create_tables
import sys
import db_setup
import api
from config import config
import faces
import os
import webbrowser
from jinja2 import FileSystemLoader, Environment
import json


def cleanup(cnx, cursor):
    cnx.commit()
    cursor.close()
    cnx.close()


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
