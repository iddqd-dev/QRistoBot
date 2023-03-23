import os
import tempfile
import shutil
from imagehash import average_hash
from PIL import Image

def compare_file_hashes(new_file, directory_path):
    """ Compare file with existing files in directory
    Args:
        new_file (string): File for comparing
        directory_path (string): Path to directory with existing files.

    Returns:
        result (string): Name of the file in directory_path that matches the hash of new_file,
             or new_file if no matching file is found.
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file_hash = average_hash(Image.open(new_file))
        tmp_file.close()

    for image in os.listdir(directory_path):
        file_path = os.path.join(directory_path, image)
        exist_file_hash = average_hash(Image.open(file_path))
        if exist_file_hash == tmp_file_hash:
            os.remove(new_file)
            return image
    shutil.move(new_file, directory_path)
    return os.path.basename(new_file)