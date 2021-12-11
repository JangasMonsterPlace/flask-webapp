from flask_restful import Resource, reqparse
from util.FileHandler import FileHandler
import werkzeug

class FileController(Resource):
    def __init__(self) -> None:
        self.fileHandler = FileHandler()
        super().__init__()

    def get(self):
        file_name = ''
        parser = reqparse.RequestParser()
        parser.add_argument('file_name')
        args = parser.parse_args()
        file_name = args['file_name']
        print(file_name)


        if file_name == '':
            return {"file_names": self.fileHandler.list_contents()}
        else:
            return {"file_content": "not ready"}

    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        file = args['file']
        print(file)
        self.fileHandler.upload_file(file.filename, file)

        return {'status': 'OK'}