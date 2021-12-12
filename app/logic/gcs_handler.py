from google.cloud import storage
import settings

class GCSHandler:

    def __init__(self) -> None:

        self.storage_client = storage.Client()
        self.BUCKET_NAME = settings.GCS_BUCKET_NAME
        self.bucket = self.storage_client.get_bucket(settings.GCS_BUCKET_NAME)

    def list_contents(self, prefix = "data"):

        blob_name_list = []

        blobs = list(self.bucket.list_blobs(prefix=prefix))

        for blob in blobs:

            blob_name_list.append(blob.name)

        return blob_name_list

    def read_file(self, file_name):

        blob = self.bucket.blob(file_name)

        return blob.download_as_string() # Returns a byte encoded string

    def upload_file(self, file_name, file_data):

        blob = self.bucket.blob(file_name)

        blob.upload_from_string(file_data)

        return blob

    def create_bucket(self, bucket_name):

        bucket = self.storage_client.create_bucket(bucket_name)

        return bucket

    def delete_bucket(self, bucket_name):
        
        bucket = self.storage_client.get_bucket(bucket_name)

        bucket.delete()

        return bucket

    def download_blob(self, source_blob_name, destination_file_name):
        
        bucket = self.storage_client.get_bucket(settings.GCS_BUCKET_NAME)

        blob = bucket.blob(source_blob_name)

        blob.download_to_filename(destination_file_name)

        return blob

_gcs_handler = GCSHandler()

if __name__ == "__main__":

    GCSHandler = GCSHandler()

    GCSHandler.list_contents()