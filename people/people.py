import faces
import json
create = """
INSERT into people (name)
VALUES (%s)
"""

assign = """
UPDATE faces
SET person_id = %(person_id)s
WHERE id = %(face_id)s
"""
assign_many = """
UPDATE faces
SET person_id = %s
WHERE id IN (%s)
"""

list_people = "SELECT * from people"

list_with_faces = """
SELECT people.id person_id, faces.id face_id, files.file_hash, people.name, faces.locations  FROM people
INNER JOIN faces on faces.person_id = people.id
LEFT JOIN files on files.id = faces.file_id
GROUP  by people.id
"""

person_faces = """
SELECT faces.id, files.file_hash, person_id, locations FROM faces 
LEFT JOIN files on files.id = faces.file_id
WHERE person_id = %(id)s
"""

person_face = "select id from faces where person_id = %(id)s"


def parse_face_locations(face):
    face['locations'] = json.loads(face['locations'])
    return face


class People:
    """
    Manage people and their faces on the database
    """

    def __init__(self, cnx, log=print):
        """
        Takes a cursor so it can be used for db operations
        """
        self.cursor = cnx.cursor(buffered=True, dictionary=True)
        self.raw_cursor = cnx.cursor(buffered=True)
        self.cnx = cnx
        self.log = log

    def execute(self, query, **args):
        self.cursor.execute(query, args)
        self.cnx.commit()
        return self.cursor

    def create(self, *, name, faces=()):
        """
        Creates a new person on the database
        """
        # try:
        print("Creating a new person named", name)
        self.cursor.execute(create, (name,))
        self.cnx.commit()
        id = self.cursor.lastrowid
        if len(faces) > 0:
            print('Extra faces for new person', faces)
            self.assign_many_faces(faces=faces, person_id=id)
        return id, faces
        # except:
        #     print("Unknown error while creating a new person {}".format(name))
        #     return -1

    def assign_face(self, *, face_id, person_id):
        return {'updated': self.execute(assign, person_id=person_id, face_id=face_id).rowcount}

    def assign_many_faces(self, *, faces, person_id):
        self.cursor.executemany(assign_many, [(person_id, face) for face in faces])
        self.cnx.commit()
        updated = self.cursor.rowcount
        return {'updated': updated}

    def list(self):
        self.cursor.execute(list_people)
        return {'people': self.cursor.fetchall()}

    def list_with_faces(self):
        self.cursor.execute(list_with_faces)
        results = self.cursor.fetchall()
        return {'people': list(map(parse_face_locations, results))}

    def from_db(self, id):
        self.cursor.execute(
            'SELECT * FROM people WHERE id = %(id)s',
            {'id': id})
        return self.cursor.fetchall()[0]

    def faces(self, id):
        self.cursor.execute(person_faces, {'id': id})
        result = self.cursor.fetchall()
        return list(map(parse_face_locations, result))

    def get_potential_faces(self, id):
        self.cursor.execute(person_face, {'id': id})
        face_id = self.cursor.fetchall()[0]['id']
        face_encodings = faces.get_face_encodings(face_id=face_id, cursor=self.raw_cursor)
        possible_faces = faces.find_closest_match_in_db(
            face_encodings=face_encodings,
            ignore_known=True,
            cursor=self.cursor)
        return list(map(parse_face_locations, possible_faces))
