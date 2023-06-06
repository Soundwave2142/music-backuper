from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.windows.mains import WindowRoot

from shutil import copytree
from os import getcwd, listdir, path
from json import load as json_load
from re import findall, match, sub
from tkinter import Entry, Label

from src.providers.constants import CONFIG_KEY_DOWNLOADER_LINK
from src.windows.popups import WindowMusicConfirm
from src.providers.config import config
from src.components.filesystem_helper import delete as fh_delete, get_dir_size as fh_get_dir_size, write_music_metadata, MusicFileMetadata
from src.components.validator import validate_input, NotEmptyRule, PathExistsRule


class ComponentProcessorCleaner:
    # TODO: implement properly.
    def process(self, directory):
        for folder in listdir(directory):
            sub_directory = path.join(directory, folder)
            if path.isdir(sub_directory):
                if self.auto_delete(folder):
                    answer = 'y'
                    print("Auto >> DELETING >>>>  %s  <<<<   " % folder)
                elif self.auto_skip(folder):
                    answer = 'n'
                    print("Auto >> SKIPPING >>>>  %s  <<<<   " % folder)
                else:
                    answer = input("Has folder >>>>  %s  <<<<, DELETE? Enter for skip, 'y' for yes: " % folder)

                if answer.lower() == 'y':
                    fh_delete(sub_directory)

    def auto_delete(self, folder):
        auto_delete = ["Covers", "Cover", "Artwork", "Scans"]
        for text in auto_delete:
            if folder.lower().startswith(text.lower()):
                return True

        return False

    def auto_skip(self, folder):
        autoskip = ["Disc 1", "Disc 2", "Disc 3", "CD1", "CD2", "CD3", "CD 1", "CD 2", "CD 3"]
        for text in autoskip:
            if folder.lower().startswith(text.lower()):
                return True

        return False


class ComponentProcessorBackupper:
    # TODO: implement properly.

    root_dir = getcwd()
    copy_to_dir = 'E:\\Music'

    def process(self, directory):
        copy_dir = directory.replace(self.root_dir, self.copy_to_dir)
        if path.exists(copy_dir):
            if fh_get_dir_size(directory) == fh_get_dir_size(copy_dir):
                return
            fh_delete(copy_dir, True)

        copytree(directory, copy_dir)


class ComponentProcessorDownloader:
    """
    Component class for processing download from YouTube video (album)
    """
    input_download_link: Entry
    input_download_link_error_label: Label
    window: WindowRoot

    def __init__(self, input_download_link: Entry, input_download_link_error_label: Label, window: WindowRoot):
        """
        Sets required properties for class.
        @param input_download_link: required to get link from input.
        @param input_download_link_error_label: in case link is broken, error will be shown.
        @param window: requires to call sub-window metadata confirmation.
        """
        self.input_download_link = input_download_link
        self.input_download_link_error_label = input_download_link_error_label
        self.window = window

    def validate(self) -> bool:
        """
        Validates download input link.
        @return: True or False depending on if validation of input succeeded of failed.
        """
        return validate_input(self.input_download_link, self.input_download_link_error_label, [
            NotEmptyRule()
        ])

    def process(self) -> None:
        """
        Starts whole process for video album download. Remembers the link, calls yt downloader command and calls the
        rest of the function to validate and confirm metadata.
        @return: None.
        """
        link = self.input_download_link.get()
        config.set(CONFIG_KEY_DOWNLOADER_LINK, link)  # remember the link for later use.

        # generate a system command
        chapter_format = config.get("yt_downloader_chapter_format_start") + config.get("yt_downloader_chapter_format")
        system_command_main = config.get("yt_downloader_dpl_command_start").format(link=link)
        system_command_configurable = config.get("yt_downloader_dpl_command").format(chapter_format=chapter_format)

        # system(system_command_main + ' ' + system_command_configurable)

        self.window.call_window(
            WindowMusicConfirm, (self.__gather_metadata(), write_music_metadata), self.window.on_window_close
        )

    def __gather_metadata(self) -> MusicFileMetadata:
        """
        Gathers metadata from downloaded json file.
        @return: dataclass of metdata.
        """
        folder = getcwd()

        json_file = open(folder + '/tmp/processing.info.json')
        json_data = json_load(json_file)

        return MusicFileMetadata(
            folder + '/download_music/working',

            self.__find_artist_in_title(json_data["title"]),
            self.__find_album_name_in_title(json_data["title"]),
            self.__find_year_in_title(json_data["title"]),
            ''  # genre extraction not implemented currently
        )

    def __find_year_in_title(self, title: str) -> str:
        """
        Find year of album in title.
        @param title: string to search in.
        @return: string year.
        """
        # first try to find year like this "(2019)"
        year = findall('(d{4})', title)

        # then try to find year in "[2019]"
        if not year:
            year = findall('[(d{4})]', title)

        # then try to find any number combination of 4 starting with 1-3.
        if not year:
            year = match(r'.*([1-3][0-9]{3})', title)
            if year:
                year = year.group(1)

        return year

    def __find_artist_in_title(self, title: str) -> str:
        """
        Find artist in title.
        @param title: string to search in.
        @return: artist name or nothing.
        """
        artist = title.partition('-')[0]
        if not artist:
            match("(.*?):", title).group()

        return artist.strip()

    def __find_album_name_in_title(self, title: str) -> str:
        """
        Find album in title.
        @param title: string to search in.
        @return: album name or nothing.
        """
        album = title.partition('-')[2]
        if not album:
            match("(.*?):", title).group()

        return sub(r'[^a-zA-Z\s]', '', album).strip()
