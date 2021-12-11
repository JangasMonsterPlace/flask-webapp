from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from logic.upload_files import upload_file_to_gcs
from logic.list_files import get_list_files

load_dotenv()

app = Flask(
    __name__,
    static_folder='static/',
    template_folder='templates/'
)

app.secret_key = 'supersecretkey'

@app.route('/')
def index():

    return render_template('index.html')

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

    data = get_list_files()

    return render_template('files_list.html', data=data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
