from server.database import get_db
from itertools import chain
import server.database as database
from process_photos.process_photos import process
from process_photos import process_photos
from photo_queue import PhotoQueue
from flask import Flask, render_template, request, g
import json
from threading import Thread
from flask.helpers import url_for
from config import config
from api import Api
import faces
from people import People

app = Flask(__name__)
database.init_app(app)

api = Api(config['host'])


def format_faces_response(face):
    (top, right, bottom, left) = json.loads(face['locations'])
    face['locations'] = dict(top=top, right=right, bottom=bottom, left=left)
    face['url'] = api.get_img_url(hash=face['file_hash'])
    return face


def get_person():
    db = get_db()
    person = People(cnx=db.cnx)
    return person


# PAGES

@app.route('/')
@app.route('/unknown')
def unknown_faces():
    db = get_db()
    images = faces.find_unknown_in_db(cursor=db.cursor, api=api)
    existing_people = get_person().list()
    return render_template(
        'unknown_faces.html.jinja',
        images=images,
        people=existing_people,
        crop_size=100)


@app.route('/known_people')
def known_faces():
    known_people = get_person().list_with_faces()
    return render_template(
        'known_people.html.jinja',
        people=known_people['people'],
        api=api,
        crop_size=100)


@app.route('/person/<int:id>/faces')
def known_person_faces(id):
    person = get_person()
    faces = person.faces(id=id)
    person_data = person.from_db(id=id)
    return render_template(
        'faces.html.jinja',
        name=person_data['name'],
        faces=faces,
        api=api,
        crop_size=100
    )


threads = dict(photos=None)


def get_scan_status():
    thread = threads['photos']
    if thread == None:
        return 'not_started'
    if thread.is_alive():
        return 'in_progress'
    return 'finished'


@app.route('/config')
def config_page():
    return render_template('config.html.jinja', scan_status=get_scan_status())

# API


@app.route('/cmd/scan', methods=['POST'])
def start_scan():
    db = get_db()
    if threads['photos'] == None or not threads['photos'].is_alive():
        queue = PhotoQueue(db.cnx)
        queue.fill_queue()
        threads['photos'] = Thread(
            target=queue.consume,
            kwargs=dict(process=process_photos.process(api=api, cursor=db.cnx.cursor()))
        )
        threads['photos'].start()
        return {'result': 'Scan has started'}

    return {'result': 'in_progress'}


@app.route('/scan')
def scan_status():
    "Returns the scan status"
    return {'result': get_scan_status()}


@app.route('/people', methods=['POST'])
def create_person():
    name = request.json.get('name')
    faces = request.json.get('faces')
    id, faces = get_person().create(name=name, faces=faces)
    print("Created person with ", (id, name))
    return dict(result={'id': id, 'faces_count': faces})


@app.route('/people/<int:id>', methods=['DELETE'])
def delete_person(id):
    get_person().delete(id)
    return dict(result={'id': id, 'deleted': True})


@app.route('/people')
def list_people():
    return {'result': get_person().list()}


@app.route('/people/<int:person_id>/faces', methods=['POST'])
def assign_face_to_person(person_id):
    person = get_person()
    faces = request.json.get('faces')
    if len(faces) > 1:
        result = person.assign_many_faces(faces=faces, person_id=person_id)
    else:
        result = person.assign_face(face_id=faces[0], person_id=person_id)
    return dict(result=result)


@app.route('/people/<int:id>/faces')
def list_person_faces(id):
    person = get_person()
    return {'result': {
        'id': id,
        'faces': person.faces(id=id),
        'possibles': person.get_potential_faces(id=id)
    }}


@app.route('/faces/<int:id>/matches')
def possible_face_matches(id):
    db = get_db()
    face_encodings = faces.get_face_encodings(face_id=id, cursor=db.cursor)
    possible_faces = faces.find_closest_match_in_db(
        face_encodings=face_encodings,
        ignore_known=True,
        exclude_list=(id,),
        cursor=db.cnx.cursor(dictionary=True))

    return {'result': {
        'id': id,
        'faces': list(map(format_faces_response, possible_faces))
    }}@app.route('/faces/<int:id>/matches')


@app.route('/faces/<int:id>/person', methods=['DELETE'])
def unasign_face(id):
    db = get_db()
    faces.unlink_from_person(id=id, cursor=db.cursor, cnx=db.cnx)
    return {'result': {
        'id': id,
        'ok': True
    }}


@app.route('/faces-matches/')
def possible_faces_matches():
    db = get_db()
    ids = [int(id) for id in request.args.getlist('id')]
    print('Looking for', ids)
    faces_encodings = faces.get_faces_encodings(
        faces_ids=ids,
        cursor=db.cursor)
    possible_faces = faces.find_closest_matches_in_db(
        faces_encodings=faces_encodings,
        ignore_known=True,
        exclude_list=ids,
        cursor=db.cnx.cursor(dictionary=True))

    result = list(map(
        format_faces_response,
        possible_faces))

    return {'result': {'faces': result}}


with app.test_request_context():
    print(url_for('assign_face_to_person', person_id=99, face_id=100))
