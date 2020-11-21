
from datetime import datetime


class PhotoQueue(object):
    """
    Manages the queue of photos: fill it with new pictures and consume it
    """

    fill_queue_query = """
        INSERT into photo_queue (file_id, file_hash) 
        SELECT files.id, files.file_hash from files 
        WHERE file_type IN (0x6A7067) AND files.id NOT IN (SELECT file_id FROM photo_queue)
    """

    def __init__(self, cnx):
        self.cnx = cnx

    def fill_queue(self):
        cursor = self.cnx()
        cursor.execute(self.fill_queue_query)
        self.cnx.commit()

    def consume(self, process, batch_size=5, skip=0):
        cursor = self.cnx.cursor()
        countQuery = "SELECT count(file_id) FROM photo_queue WHERE checked = FALSE"
        cursor.execute(countQuery)
        (count,) = cursor.fetchall()[0]
        print("There are {} items on the queue".format(count))
        query = """
        SELECT file_id, file_hash FROM photo_queue 
        WHERE checked = False LIMIT %s OFFSET %s
        """
        time_start = datetime.now()
        for batch in range(int(count/batch_size)):
            cursor.execute(query, (batch_size, skip))
            for (file_id, hash) in cursor.fetchall():
                # try:
                process(hash=hash, file_id=file_id)
                # except:
                #     print("An error ocurred in batch {} processing {}".format(batch, file_id))
            print(cursor.rowcount)
            self.cnx.commit()
        print("Processed {} photos in queue in {} time".format(
            count,
            datetime.now() - time_start)
        )
