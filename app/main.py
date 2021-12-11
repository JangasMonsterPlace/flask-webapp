from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from controller.FileController import FileController

load_dotenv()

app = Flask(
    __name__,
    static_folder='static/',
    template_folder='templates/'
)
api = Api(app)

api.add_resource(FileController, '/api/files')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
