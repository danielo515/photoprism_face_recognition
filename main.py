from db_setup.create_tables import create_tables
from PIL import Image
import numpy as np
import requests
import face_recognition
import os
import pickle
import db_setup
import configparser

api = ""


def save_cookies(session, filename):
    with open(filename, 'wb') as f:
        f.truncate()
        pickle.dump(session.cookies, f)
        print('Saved cookies to file')


def load_cookies(session, filename):
    if not os.path.isfile(filename):
        print('cookie file was not found')
        return False
    with open(filename, 'rb') as f:
        cookies = pickle.load(f)
        print('Loaded cookies from file')
        if cookies:
            session.cookies.update(cookies)
            print('Injected cookies')
            return True
        else:
            return False


def login(username, password):
    cookie_file = 'photoprism_cookies'
    s = requests.Session()
    if load_cookies(session=s, filename=cookie_file):
        return s
    s.auth = (username, password)
    s.post("{api}/session".format(api=api), data=dict(username=username, password=password))
    save_cookies(session=s, filename=cookie_file)
    return s


def fetch_photo(session, hash):
    url = "{api}/t/{hash}/public/tile_224".format(api=api, hash=hash)
    response = session.get(url, stream=True)
    response.raw.decode_content = True
    img = Image.open(response.raw)
    return img


def pic_from_queue(cursor, process, batch_size=5):
    query = "select file_hash from photo_queue where checked = False limit %s"
    cursor.execute(query, (batch_size,))
    for hash, in cursor:
        process(hash)
    print("Processed {} photos in queue".format(cursor.rowcount))

# =========== Face recognition section =============================


def print_result(filename, location):
    top, right, bottom, left = location
    print("{},{},{},{},{}".format(filename, top, right, bottom, left))


def find_faces(image_to_check, image_name, model, upsample):
    face_locations = face_recognition.face_locations(image_to_check, number_of_times_to_upsample=upsample, model=model)
    if len(face_locations) == 0:
        print(image_name, " has no faces")
    return face_locations


def process(session):
    def _process(hash):
        photo = fetch_photo(session, hash=hash)
        faces_found = find_faces(np.array(photo), image_name=hash, model="cnn", upsample=1)
        photo.save("output/0_{}_{}.jpg".format(len(faces_found), hash))
    return _process


config = configparser.ConfigParser()
config.read('./config.ini')
db_config = dict(config['db_config'].items())
photoprism_config = dict(config['photoprism'].items())
host = photoprism_config.pop('host')
api = "http://{host}/api/v1".format(host=host)
print(photoprism_config)

(cnx, cursor) = db_setup.connect(**db_config)
db_setup.create_tables(cursor=cursor)

session = login(**photoprism_config)
pic_from_queue(cursor=cursor, process=process(session), batch_size=50)


cursor.close()
cnx.close()
