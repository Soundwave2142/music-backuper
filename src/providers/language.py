class LanguageProvider:
    # TODO: move language arrays to separate classes

    __en = {
        'root_window.title': "SLT v1.0.0"
    }

    __no = {
        # add at some point for shit and giggles
    }

    def __init__(self, language: str = "en"):
        self.language = language

    def t(self, key: str) -> str:
        localization = getattr('__' + self.language, key, self.__en)

        if key in localization:
            return localization[key]

        if key in self.__en:
            return self.__en[key]

        return key
