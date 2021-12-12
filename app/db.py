from settings import _db

def get_jobs(info):
    sql = f"SELECT id FROM jobs WHERE info=%s"
    _db.cur.execute(sql, (info, ))
    entity = _db.cur.fetchone()
    if entity:
        return entity[0]
    else:
        return None

def make_job(data):
    sql = f"INSERT INTO jobs (type,info,frequency) VALUES ('nlp',%s,120)"
    return _db.cur.execute(sql, (data, ))

def get_ngram(prev_match_id):
    sql = f"SELECT dimension,squence,frequency FROM ngram WHERE job_id=%s AND dimension=2 ORDER BY frequency DESC LIMIT 10"
    return _db.cur.execute(sql, (prev_match_id, ))