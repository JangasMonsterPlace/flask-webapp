from .gcs_handler import _gcs_handler

def get_list_files():
    """
    Get a list of all files in a bucket in data folder.
    """

    data = _gcs_handler.list_contents()

    data.remove('data/')

    data = [filename.replace('data/', '') for filename in data]

    return data