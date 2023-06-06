from dataclasses import dataclass
from os import path, unlink, listdir, scandir
from shutil import rmtree
from mutagen.mp4 import MP4


def delete(delete_path: str, silent: bool = False) -> None:
    """
    Delete folder of file from system.
    @param delete_path: folder of file to delete.
    @param silent: whatever print (and therefore sent to console) about this deletion.
    @return: None.
    """
    if not silent:
        print('Deleting %s' % delete_path)

    try:
        if path.isfile(delete_path) or path.islink(delete_path):
            unlink(delete_path)
        elif path.isdir(delete_path):
            rmtree(delete_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (delete_path, e))


def iterate(directory, folder_function, file_function) -> None:
    """
    Iterate over directory and call for folder of file actions.
    @param directory: to iterate over.
    @param folder_function: callback for folder.
    @param file_function: callback to file.
    @return: None.
    """
    for folder in listdir(directory):
        sub_directory = path.join(directory, folder)
        if path.isdir(sub_directory):
            folder_function(sub_directory)
        elif path.isfile(sub_directory):
            file_function(sub_directory)


def get_dir_size(directory: str = '.', total: float = 0) -> float:
    """
    Get the size of the directory.
    @param directory: path to directory to get size.
    @param total: starting total size.
    @return: total of directory (and possible other, depending on if total passed).
    """
    with scandir(directory) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)

    return total


@dataclass
class MusicFileMetadata:
    """
    Data class for metadata of mp3/m4a class.
    """
    file_path: str

    artist: str
    album: str
    year: str
    genre: str


def write_music_metadata(metadata: MusicFileMetadata) -> None:
    """
    Write music metadata to directory or specific file.
    @param metadata: data container.
    @return: None.
    """
    if path.isdir(metadata.file_path):
        for track in listdir(metadata.file_path):
            metadata.file_path = metadata.file_path + track
            __write_music_file_metadata(metadata)
    else:
        __write_music_file_metadata(metadata)


def __write_music_file_metadata(metadata: MusicFileMetadata) -> None:
    """
    Write music metadata to specific file.
    @param metadata: data container.
    @return: None.
    """
    file = open(metadata.file_path, 'r+b')

    tags = MP4(file).tags
    tags['\xa9nam'] = 'name'  # track title
    tags['\xa9alb'] = metadata.album  # album
    tags['\xa9ART'] = metadata.artist  # artist
    tags['\xa9day'] = metadata.year  # year
    tags.save(file)
