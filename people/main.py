
class People():
    """
    Manage people and their faces on the database
    """

    def __init__(self, cursor):
        """
        Takes a cursor so it can be used for db operations
        """
        self.cursor = cursor

    def create(self, *, name):
        """
        Creates a new person on the database
        """
        query = """
        INSERT into people (name)
        VALUES (%s)
        """
        try:
            self.cursor.execute(query, (name,))
        except:
            print("Unknown error while creating a new person {}".format(name))
            return None

    def assign_face(self, *, face_id, person_id):
        query = """
        UPDATE faces
        SET person_id = %s,
        WHERE face_id = %s,
        """
        self.cursor.execute(query, (person_id, face_id))
