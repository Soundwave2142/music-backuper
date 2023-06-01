import os.path
import json


class __ConfigProvider:
    """
    Config provider for the whole app, reads and writes to and from json file inside the app directory.
    """
    __config = {}
    __config_default_name = "config.json"
    __config_default = {
        "language": "en",
        "theme": "default",
    }

    def __init__(self):
        """
        Creates a new config (writes to json file) if not existent. Then loads from json file configuration for the app.
        """
        path = './' + self.__config_default_name
        if not os.path.isfile(path):
            self.__write_to_file(self.__config_default)

        self.__read_from_file()

    def get(self, name: str, default: any = None) -> any:
        print('get')
        """
        Get value from config.
        @param name: key of the config value.
        @param default: in case name does not exist in config.
        @return: value from config.
        """
        if name in self.__config:
            return self.__config[name]

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
            self.__config = json.load(json_file)

    def __write_to_file(self, config_json: dict) -> None:
        """
        Function that writes config to file in json format.
        @param config_json: dictionary config to write
        @return: None.
        """
        with open(self.__config_default_name, "w") as outfile:
            json_config = json.dumps(config_json, indent=4)
            outfile.write(json_config)


config = __ConfigProvider()
