from html import entities
from settings import _db

def get_job(info):
    sql = f"SELECT id FROM jobs WHERE info=%s"
    _db.cur.execute(sql, (info, ))
    entity = _db.cur.fetchone()
    if entity:
        return entity
    else:
        return None

def get_jobs():
    sql = f"SELECT * FROM jobs WHERE type='nlp' ORDER BY frequency"
    _db.cur.execute(sql)
    entities = _db.cur.fetchall()
    if entities:
        return entities
    else:
        return None

def get_lda(job_id, topic_id):
    sql = f"SELECT * FROM ldas WHERE job_id=%s AND topic_id=%s ORDER BY timestamp DESC LIMIT 100"
    _db.cur.execute(sql, (job_id, topic_id))
    entities = _db.cur.fetchall()
    if entities:
        return entities
    else:
        return None

def make_job(data):
    sql = f"INSERT INTO jobs (type,info,frequency) VALUES ('nlp',%s,120)"
    _db.cur.execute(sql, (data, ))

def get_ngram(prev_match_id, dimension):
    sql = f"SELECT * FROM ngram WHERE job_id=%s AND dimension=%s ORDER BY frequency DESC LIMIT 10"
    _db.cur.execute(sql, (prev_match_id,dimension ))
    return _db.cur.fetchall()