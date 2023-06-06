from os.path import isfile
from json import load as json_load, dumps as json_dumps

from src.providers.constants import *


class __ConfigProvider:
    """
    Config provider for the whole app, reads and writes to and from json file inside the app directory.
    """
    __config = {}
    __config_default_name = 'config.json'
    __config_default = {
        # marked with * are variables that do not apper in config window therefore not configurable in app.
        'language': 'en',
        'theme': THEME_DEFAULT_NAME,
        'yt_downloader_chapter_format_start': 'chapter:downloaded_music\\working\\',  # *
        'yt_downloader_chapter_format': '%(section_number)s. %(section_title)s.%(ext)s',
        'yt_downloader_dpl_command_start': "additional_tools\\yt-dlp -f 139 -o \"tmp\\processing.%(ext)s\" {link}",  # *
        'yt_downloader_dpl_command': "--split-chapters -o \"{chapter_format}\" --embed-thumbnail --write-info-json"
    }

    def __init__(self):
        """
        Creates a new config (writes to json file) if not existent. Then loads from json file configuration for the app.
        """
        path = './' + self.__config_default_name
        if not isfile(path):
            self.__write_to_file(self.__config_default)

        self.__read_from_file()

    def get(self, name: str, default: any = None) -> any:
        """
        Get value from config.
        @param name: key of the config value.
        @param default: in case name does not exist in config/default_config.
        @return: value from config, default config or default given value.
        """
        if name in self.__config:
            return self.__config[name]

        if not default and name in self.__config_default:
            return self.__config_default[name]

        return default

    def set(self, name: str, value: any, write_to_file: bool = True) -> None:
        """
        Set value to config and write config to file unless specified not to.
        @param write_to_file:
        @param name: key of config value.
        @param value: config value.
        @return: None.
        """
        self.__config[name] = value

        if write_to_file:
            self.__write_to_file(self.__config)

    def __read_from_file(self) -> None:
        """
        Reads from json file to config variable
        @return: None.
        """
        with open(self.__config_default_name) as json_file:
            self.__config = json_load(json_file)

    def __write_to_file(self, config_json: dict) -> None:
        """
        Function that writes config to file in json format.
        @param config_json: dictionary config to write
        @return: None.
        """
        with open(self.__config_default_name, "w") as outfile:
            json_config = json_dumps(config_json, indent=4)
            outfile.write(json_config)


config = __ConfigProvider()
