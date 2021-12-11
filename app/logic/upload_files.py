from .gcs_handler import _gcs_handler

def upload_file_to_gcs(file_name, file_content):
    """
    Uploads a file to GCS.
    """
    # print("Uploading file to GCS...")

    file_name = f"data/{file_name}"

    _gcs_handler.upload_file(file_name, file_content)

    return 0