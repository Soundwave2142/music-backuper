import json
import os.path


class ConfigProvider:
    __config = {}
    __config_default_name = "config.json"
    __config_default = {
        "language": "en",
        "theme": "default",
    }

    def __init__(self):
        # create new config if not exists
        path = './' + self.__config_default_name
        if not os.path.isfile(path):
            self.__write_to_file(self.__config_default)

        # load config into variable
        with open(self.__config_default_name) as json_file:
            self.__config = json.load(json_file)

    def get(self, name: str, default=None):
        if name in self.__config:
            return self.__config[name]

        return default

    def set(self, name: str, variable):
        self.__config[name] = variable
        self.__write_to_file(self.__config)

    def __write_to_file(self, config: object):
        with open(self.__config_default_name, "w") as outfile:
            json_config = json.dumps(config, indent=4)
            outfile.write(json_config)
