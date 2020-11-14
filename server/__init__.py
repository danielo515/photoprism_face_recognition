from flask import Flask, render_template, request
import json

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


@app.route('/')
@app.route('/unknown')
def unknown_faces():
    images = faces.find_unknown_in_db(cursor=cursor, api=api)
    return render_template('unknown_faces.html.jinja', images=images, crop_size=100)


@app.route('/person/<int:id>/faces')
def known_person_faces(id):
    faces = person.faces(id=id)
    possible_faces = person.get_potential_faces(id=id)
    person_data = person.from_db(id=id)
    print(faces)
    return render_template(
        'faces.html.jinja',
        name=person_data['name'],
        faces=faces,
        possible_faces=possible_faces,
        api=api,
        crop_size=100
    )


@app.route('/people', methods=['POST'])
def create_person():
    name = request.json.get('name')
    id = person.create(name=name)
    print("Created person with ", (id, name))
    return dict(result={'id': id})


@app.route('/people/<int:person_id>/face/<int:face_id>', methods=['POST'])
def assign_face_to_person(person_id, face_id):
    result = person.assign_face(face_id=face_id, person_id=person_id)
    return dict(result=result)


@app.route('/people')
def list_people():
    return {'result': person.list()}


@app.route('/people/<int:id>/faces')
def list_person_faces(id):
    return {'result': {
        'id': id,
        'faces': person.faces(id=id),
        'possibles': person.get_potential_faces(id=id)
    }}


with app.test_request_context():
    print(url_for('assign_face_to_person', person_id=99, face_id=100))
