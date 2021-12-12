import json
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
    for entity in _db.cur.fetchall():
        try:
            entity["info"] = json.loads(entity["info"])
        except:
            continue
        yield entity


def get_lda(job_id, topic_id):
    sql = f"SELECT * FROM ldas WHERE job_id=%s AND topic_id=%s ORDER BY timestamp DESC LIMIT 100"
    _db.cur.execute(sql, (job_id, topic_id))
    entities = _db.cur.fetchall()
    if entities:
        return entities
    else:
        return None


def name_lda(job_id, topic_id, name, description):
    sql_select = f"SELECT * FROM lda_interpretation WHERE job_id=%s AND topic_id=%s"
    _db.cur.execute(sql_select, (job_id, topic_id,))
    entities = _db.cur.fetchone()
    if entities:
        sql_update = f"UPDATE lda_interpretation SET title=%s, description=%s WHERE job_id=%s AND topic_id=%s"
        _db.cur.execute(sql_update, (name, description, job_id, topic_id))
    else:
        sql_insert = f"INSERT INTO lda_interpretation (job_id, topic_id, title, description) VALUES (%s, %s, %s, %s)"
        _db.cur.execute(sql_insert, (job_id, topic_id, name, description,))
        
    


def get_name_lda(job_id, category_id):
    sql = f"SELECT * FROM lda_interpretation WHERE job_id=%s AND topic_id=%s"
    _db.cur.execute(sql, (job_id, category_id))
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
    _db.cur.execute(sql, (prev_match_id, dimension))
    return _db.cur.fetchall()
