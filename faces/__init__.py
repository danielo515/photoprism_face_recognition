import json
from queries import Queries


def get_face_encodings(*, face_id, cursor):
    query = Queries.get_face_encodings.render()
    cursor.execute(query, (face_id,))
    encodings = cursor.fetchall()[0]
    return encodings


def find_closest_match_by_id(*, face_id, cursor, limit=50):
    return find_closest_match_in_db(
        face_encodings=get_face_encodings(face_id=face_id, cursor=cursor),
        cursor=cursor,
        limit=limit)


def find_closest_match_in_db(*, face_encodings, cursor, limit=50):
    query = Queries.find_closest_match.render(encodings=enumerate(face_encodings))
    cursor.execute(query, {'limit': limit})
    return cursor.fetchall()


def find_unknown_in_db(*, cursor, api, limit=200):
    cursor.execute(Queries.unknown_faces.render(), {'limit': limit})
    results = []
    # for (a_id, a_locations, a_hash, b_id, b_locations, b_hash, _) in cursor:
    for (a_id, a_locations, a_hash) in cursor:
        results.append((api.get_img_url(hash=a_hash), json.loads(a_locations), a_id))
        # results.append((api.get_img_url(hash=b_hash),  json.loads(b_locations), b_id))
    return results
