''' Methods for generating and validating unique IDs '''
from uuid import uuid4


def generate_file_id( file_name: str) -> str:
    ''' Generate a unique file ID based on the file name and a UUID4
    Args:
        file_name (str): The name of the file
        prefix (str): Purpose of file upload
    Returns:
        str: A unique file ID
    '''
    unique_id = str(uuid4())
    return f"{unique_id}_{file_name}"