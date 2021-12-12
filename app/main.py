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
                "dimension_three": ngrams_dimension_three
                }
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


@app.route('/name_lda')
def name_lda_endpoint():
    data = {
        "category_id": request.form["category_id"],
        "job_id": request.form["job_id"],
        "name": request.form["name"],
        "description": request.form["description"]
    }

    name_lda(
        request.json["job_id"],
        request.json["category_id"],
        request.json["name"],
        request.json["description"],
        )

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
    res = es.search(index="pg-textsource-texts", query=query, size=1000)
    data = []
    if len(res["hits"]['hits']) > 0:
        data = [e["_source"] for e in res["hits"]['hits']]

    return jsonify({"data": data})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
