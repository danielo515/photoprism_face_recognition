
create = """
INSERT into people (name)
VALUES (%s)
"""

assign = """
UPDATE faces
SET person_id = %s,
WHERE face_id = %s,
"""


class People:
    """
    Manage people and their faces on the database
    """

    def __init__(self, cnx, log=print):
        """
        Takes a cursor so it can be used for db operations
        """
        self.cursor = cnx.cursor(buffered=True)
        self.cnx = cnx
        self.log = log

    def create(self, *, name):
        """
        Creates a new person on the database
        """
        try:
            print("Creating a new person named", name)
            self.cursor.execute(create, (name,))
            self.cnx.commit()
            id = self.cursor.lastrowid
            return id
        except:
            print("Unknown error while creating a new person {}".format(name))
            return -1

    def assign_face(self, *, face_id, person_id):
        self.cursor.execute(assign, (person_id, face_id))
