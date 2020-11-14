from flask import Flask, render_template
from config import config
from api import Api
import db_setup
import faces

app = Flask(__name__)


(cnx, cursor) = db_setup.connect(**config['db_config'])
api = Api(config['host'])


@app.route('/')
@app.route('/unknown')
def unknown_faces():
    images = faces.find_unknown_in_db(cursor=cursor, api=api)
    return render_template('unknown_faces.html.jinja', images=images, crop_size=100)
