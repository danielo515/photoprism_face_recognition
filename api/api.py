import os
import pickle
from PIL import Image, UnidentifiedImageError
import requests


class Api:
    def __init__(self, host):
        self.api = "http://{host}/api/v1".format(host=host)
        self.session = requests.Session()

    def save_cookies(session, filename):
        for c in session.cookies:
            print(c)
        with open(filename, 'wb') as f:
            f.truncate()
            pickle.dump(session.cookies, f)
            print('Saved cookies to file', session.cookies)

    def load_cookies(session, filename):
        if not os.path.isfile(filename):
            print('cookie file was not found')
            return False
        with open(filename, 'rb') as f:
            cookies = pickle.load(f)
            print('Loaded cookies from file', cookies)
            if cookies:
                session.cookies.update(cookies)
                print('Injected cookies')
                return True
            else:
                return False

    def login(self, username, password):
        cookie_file = 'photoprism_cookies'
        s = self.session
        if self.load_cookies(session=s, filename=cookie_file):
            return s
        s.auth = (username, password)
        s.post("{api}/session".format(api=api), data=dict(username=username, password=password))
        self.save_cookies(session=s, filename=cookie_file)
        return s

    def fetch_photo(self, hash):
        url = "{api}/t/{hash}/public/tile_224".format(api=self.api, hash=hash)
        response = self.session.get(url, stream=True)
        response.raw.decode_content = True
        try:
            img = Image.open(response.raw)
        except UnidentifiedImageError as error:
            print("Error during fetching image {} ".format(hash), error)
            print(response)
            return None
        return img
