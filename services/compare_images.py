import hashlib
import os


def get_file_hash(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash


def compare_file_hashes(new_file, directory_path):
    """ Compare file with existing files in directory
    Args:
        new_file (string): File for comparing
        directory_path (string): path to existing files

    Returns:
        result (bool): result of comparing in bool
    """
    for image in os.listdir(directory_path):
        file_existing = os.path.join(directory_path, image)
        file_downloaded = os.path.join(directory_path, new_file)
        hash_existing = get_file_hash(file_existing)
        hash_downloaded = get_file_hash(file_downloaded)
        if hash_existing == hash_downloaded:
            print('Removing ' + file_downloaded)
            print(file_existing)
            os.remove(file_downloaded)
            return image
    return new_file