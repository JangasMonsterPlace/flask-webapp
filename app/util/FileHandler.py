from google.cloud import storage


class FileHandler:
    def __init__(self, BUCKET_NAME: str = "altair-janga") -> None:

        self.storage_client = storage.Client()
        self.BUCKET_NAME = BUCKET_NAME
        self.bucket = self.storage_client.get_bucket(BUCKET_NAME)

    def list_contents(self):

        blob_name_list = []

        blobs = list(self.bucket.list_blobs())

        for blob in blobs:

            blob_name_list.append(blob.name)
        return blob_name_list

    def read_file(self, file_name):

        blob = self.bucket.blob(file_name)

        return blob.download_as_string() # Returns a byte encoded string


    def upload_file(self, file_name, file_data):

        blob = self.bucket.blob(file_name)
        blob.upload_from_string(self, file_data)

        return blob



    def create_bucket(self, bucket_name):

        bucket = self.storage_client.create_bucket(bucket_name)

        return bucket


    def delete_bucket(self, bucket_name):
        
        bucket = self.storage_client.get_bucket(bucket_name)
        bucket.delete()

        return bucket


    def download_blob(self, bucket_name, source_blob_name, destination_file_name):
        
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)


        return blob



if __name__ == "__main__":
    fileHandler = FileHandler()
    fileHandler.list_contents()