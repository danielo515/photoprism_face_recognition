from process_photos.process_photos import process
from process_photos import process_photos
from photo_queue import PhotoQueue
from flask import Flask, render_template, request
import json
from threading import Thread
from flask.helpers import url_for
from config import config
from api import Api
import db_setup
import faces
from people import People

app = Flask(__name__)


(cnx, cursor) = db_setup.connect(**config['db_config'])
api = Api(config['host'])
person = People(cnx=cnx)


# PAGES
@app.route('/')
@app.route('/unknown')
def unknown_faces():
    images = faces.find_unknown_in_db(cursor=cursor, api=api)
    existing_people = person.list()
    return render_template(
        'unknown_faces.html.jinja',
        images=images,
        people=existing_people,
        crop_size=100)


@app.route('/known_people')
def known_faces():
    known_people = person.list_with_faces()
    print(known_people)
    return render_template(
        'known_people.html.jinja',
        people=known_people['people'],
        api=api,
        crop_size=100)


@app.route('/person/<int:id>/faces')
def known_person_faces(id):
    faces = person.faces(id=id)
    possible_faces = person.get_potential_faces(id=id)
    person_data = person.from_db(id=id)
    return render_template(
        'faces.html.jinja',
        name=person_data['name'],
        faces=faces,
        possible_faces=possible_faces,
        api=api,
        crop_size=100
    )


threads = dict(photos=None)

# API


def get_scan_status():
    thread = threads['photos']
    if thread == None:
        return 'not_started'
    if thread.is_alive():
        return 'in_progress'
    return 'finished'


@app.route('/cmd/scan', methods=['POST'])
def start_scan():
    if threads['photos'] == None or not threads['photos'].is_alive():
        queue = PhotoQueue(cnx)
        queue.fill_queue()
        threads['photos'] = Thread(
            target=queue.consume,
            kwargs=dict(process=process_photos.process(api=api, cursor=cnx.cursor()))
        )
        threads['photos'].start()
        return {'result': 'Scan has started'}

    return {'result': 'in_progress'}


@app.route('/scan')
def scan_status():
    "Returns the scan status"
    return {'result': get_scan_status()}


@app.route('/config')
def config_page():
    return render_template('config.html.jinja', scan_status=get_scan_status())


@app.route('/people', methods=['POST'])
def create_person():
    name = request.json.get('name')
    faces = request.json.get('faces')
    id, faces = person.create(name=name, faces=faces)
    print("Created person with ", (id, name))
    return dict(result={'id': id, 'faces_count': faces})


@app.route('/people')
def list_people():
    return {'result': person.list()}


@app.route('/people/<int:person_id>/faces', methods=['POST'])
def assign_face_to_person(person_id):
    faces = request.json.get('faces')
    if len(faces) > 1:
        result = person.assign_many_faces(faces=faces, person_id=person_id)
    else:
        result = person.assign_face(face_id=faces[0], person_id=person_id)
    return dict(result=result)


@app.route('/people/<int:id>/faces')
def list_person_faces(id):
    return {'result': {
        'id': id,
        'faces': person.faces(id=id),
        'possibles': person.get_potential_faces(id=id)
    }}


with app.test_request_context():
    print(url_for('assign_face_to_person', person_id=99, face_id=100))
