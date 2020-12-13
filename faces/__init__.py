import json
import face_recognition
import numpy as np
from queries import Queries


def get_face_encodings(*, face_id, cursor):
    query = Queries.get_face_encodings.render()
    cursor.execute(query, (face_id,))
    encodings = cursor.fetchall()[0]
    return encodings


def get_faces_encodings(*, faces_ids, cursor):
    encodings = [
        get_face_encodings(face_id=id, cursor=cursor)
        for id in faces_ids
    ]
    return encodings


def find_closest_match_by_id(*, face_id, cursor, limit=50):
    return find_closest_match_in_db(
        face_encodings=get_face_encodings(face_id=face_id, cursor=cursor),
        cursor=cursor,
        limit=limit)


def find_closest_match_in_db(*, face_encodings, cursor, ignore_known=False, limit=50, exclude_list=None):
    query = Queries.find_closest_match.render(
        ignore_known=ignore_known,
        exclude_list=",".join(map(str, exclude_list)) if exclude_list else None,
        encodings=enumerate(face_encodings)
    )
    cursor.execute(query, {'limit': limit})
    return cursor.fetchall()


def find_closest_matches_in_db(*, faces_encodings, cursor, ignore_known=False, limit=50, exclude_list=None):
    result = []
    for encodings in faces_encodings:
        faces = find_closest_match_in_db(
            face_encodings=encodings, cursor=cursor, ignore_known=ignore_known, limit=limit, exclude_list=exclude_list)
        exclude_list = exclude_list + [f['id'] for f in faces]
        result = result + faces
    return result


def find_unknown_in_db(*, cursor, api, limit=200):
    cursor.execute(Queries.unknown_faces.render(), {'limit': limit})
    results = []
    # for (a_id, a_locations, a_hash, b_id, b_locations, b_hash, _) in cursor:
    for (a_id, a_locations, a_hash) in cursor:
        results.append((api.get_img_url(hash=a_hash), json.loads(a_locations), a_id))
        # results.append((api.get_img_url(hash=b_hash),  json.loads(b_locations), b_id))
    return results


def find_in_photo(photo):
    photo_arr = np.array(photo)
    locations = face_recognition.face_locations(
        photo_arr,
        model="cnn",
        number_of_times_to_upsample=0
    )
    if(len(locations) > 0):
        encodings = face_recognition.face_encodings(
            photo_arr,
            known_face_locations=locations)
        return (encodings, locations)
    else:
        return ([], [])


def save_to_db(image_id, encodings, locations, cursor):
    for (encoding, location) in zip(encodings, locations):
        cursor.execute(
            Queries.save_face,
            (image_id, json.dumps(location)) + tuple(encoding))


def unlink_from_person(*, id: int, cursor, cnx):
    cursor.execute('UPDATE faces SET person_id = null WHERE id = %s', (id,))
    print(cursor.rowcount)
    cnx.commit()
