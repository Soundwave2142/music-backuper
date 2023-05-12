import os
import shutil


def delete(file_path, silent=False):
    if not silent:
        print('Deleting %s' % file_path)

    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

    if not silent:
        print('--------------------------------------')


def iterate(directory, folder_function, file_function):
    for folder in os.listdir(directory):
        sub_directory = os.path.join(directory, folder)
        if os.path.isdir(sub_directory):
            folder_function(sub_directory)
        elif os.path.isfile(sub_directory):
            file_function(sub_directory)


def get_dir_size(path='.', total=0):
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)

    return total
