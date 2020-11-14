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


@app.route('/person', methods=['POST'])
def create_person():
    name = request.json.get('name')
    id = person.create(name=name)
    print("Created person with ", (id, name))
    return dict(result={'id': id})


@app.route('/person/<int:person_id>/face/<int:face_id>', methods=['POST'])
def assign_face_to_person(person_id, face_id):
    return json.dumps([person_id, face_id])


with app.test_request_context():
    print(url_for('assign_face_to_person', person_id=99, face_id=100))
