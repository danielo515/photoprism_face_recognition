import faces


def flag_photo_as_processed(file_id, cursor, face_count=0):
    # print("Flagging", file_id)
    cursor.execute("""
    UPDATE photo_queue
    SET checked = 1, face_count = %s
    WHERE file_id = %s;
    """, (face_count, file_id))


def process(api, cursor):
    def _process(hash, file_id):
        photo = api.fetch_photo(hash=hash)
        if photo == None:
            print('Skipped photo {}'.format(file_id))
            return flag_photo_as_processed(file_id=file_id, cursor=cursor)

        (encodings, locations) = faces.find_in_photo(photo)
        if(len(encodings) > 0):
            faces.save_to_db(
                image_id=file_id, cursor=cursor,
                encodings=encodings, locations=locations,
            )
            photo.save("output/{}_{}.jpg".format(len(locations), hash))
        flag_photo_as_processed(
            file_id=file_id, cursor=cursor, face_count=len(locations)
        )
    return _process
