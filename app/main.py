from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from logic.upload_files import upload_file_to_gcs
from logic.list_files import get_list_files
from settings import _db, es
import json
from db import *

load_dotenv()


app = Flask(
    __name__,
    static_folder='static/',
    template_folder='templates/'
)

app.secret_key = 'supersecretkey'


@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')


@app.route('/jobs', methods=['GET'])
def jobs():
    jobs = list(get_jobs())
    data = {"jobs": jobs}
    return render_template("jobs.html", data=data)


@app.route('/hastags', methods=['GET, POST'])
def hashtags():
    if request.method == 'GET':
        return render_template('hastags.html')
    else:
        return redirect(f"/job/{job['id']}", code=302)



@app.route('/job/<job_id>', methods=['GET'])
@app.route('/job', methods=['POST'])
def job(job_id=0):
    if request.method == 'GET':
        print(job_id)
        job = int(job_id)
        ngrams_dimension_two = get_ngram(job, 2)
        ngrams_dimension_three = get_ngram(job, 3)

        return_data = {
            "job": job,
            "ngrams": {
                "dimension_two": ngrams_dimension_two,
                "dimension_three": ngrams_dimension_three,
            },
            "category_names": {"cat_1": get_name_lda(job, 1), "cat_2": get_name_lda(job, 2),"cat_3":  get_name_lda(job, 3), "cat_4":  get_name_lda(job, 4)}
        }
        return render_template('results.html', data=return_data)
    elif request.method == 'POST':
        data = {
            # "hastag": request.form["hashtag"],
            "from_date": request.form["from_date"],
            "to_date": request.form["to_date"],
            "source_type": request.form["source_type"],
            "sentiment": request.form["sentiment"],
        }
        query_dict_str = json.dumps(data)
        job = get_job(query_dict_str)
        if job == None:
            make_job(query_dict_str)
            job = get_job(query_dict_str)

        return redirect(f"/job/{job['id']}", code=302)


@app.route('/ping')
def ping():
    return jsonify({'status': 'ok'})


@app.route('/upload_file', methods=['POST', 'GET'])
def upload_files_route():
    if request.method == 'GET':
        return render_template('upload.html')

    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        if not filename.endswith('.csv'):
            return render_template('upload.html', msg='Please upload a CSV file')

        file_data = f.read()

        if f:
            upload_file_to_gcs(filename, file_data)
            return render_template('upload.html', msg="File uploaded successfully")

        else:
            return render_template('error.html')


@app.route('/list_files')
def list_files():
    data = {"files": get_list_files()}
    return render_template('files_list.html', data=data)


@app.route('/name_lda', methods=['POST'])
def name_lda_endpoint():
    try:
        name_lda(
            request.form["job_id"],
            request.form["category_id"],
            request.form["name"],
            request.form["description"],
        )
        return jsonify({'status': '201'})
    except Exception as e:
        return jsonify({"error": str(e), "status": "400"})


@app.route('/get_lda', methods=['GET'])
def get_lda_endpoint():
    job_id = request.args.get('job_id')
    category_id = request.args.get('category_id')
    lda = get_lda(job_id, category_id)
    data = {
        "lda": lda
    }
    return data


@app.route("/get-text-bodies-for-sequence", methods=["GET"])
def get_tweets_by_keywords():
    q = request.args.getlist("q")
    query = {
        "match": {
            "text": {
                "query": " ".join(q),
                "operator": "and"
            }
        }
    }
    aggs = {
        "group_by_day": {
            "date_histogram": {
                "field": "written_by_user_at",
                "interval": "day"
            },
            "aggs": {
                "group_by_day": {
                    "sum": {
                        "script": "1"
                    }
                }
            }
        }
    }
    res = es.search(index="pg-textsource-texts", query=query, size=1000, aggs=aggs)
    data = []
    if len(res["hits"]['hits']) > 0:
        data = [e["_source"] for e in res["hits"]['hits']]

    parsed_buckets = {"dates": [], "values": []}
    try:
        buckets = res["aggregations"]["group_by_day"]["buckets"]
        for b in buckets:
            parsed_buckets["dates"].append(b['key_as_string'].replace("T00:00:00.000Z", ""))
            parsed_buckets["values"].append(b['doc_count'])

    except Exception as e:
        buckets = []

    return jsonify({
        "raw_text_data": data,
        "time_aggregated_data": parsed_buckets
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
