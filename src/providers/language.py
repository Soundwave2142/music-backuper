class LanguageProvider:
    """
    Holds a text for the whole app for English, Ukrainian and Norwegian languages. Call method "t" for translation.
    Perhaps investigate some better implementations of this? For example: Move string arrays to some file and read it.
    """
    en = {
        'root_window.title': "SLT v1.0.0",
        'root_window.clean_and_backup': "Clean up folders and back them up to external hard-drive",

        'root_window.download_yt_album': "Download youtube album and split it to m4a files"
    }

    ua = {
        'root_window.clean_and_backup': "Підчистити папки та створити резервну копію на зовнішньому жорсткому диску",
    }

    no = {
        'root_window.clean_and_backup': "Rydd opp i mapper og ta sikkerhetskopi av dem på ekstern harddisk.",
        # add at some point for shit and giggles
    }

    def __init__(self, language: str = "en"):
        """
        Create an instance of provider with needed language
        @param language: short two letter for language identifier used within class
        """
        self.language = language

    def t(self, key: str) -> str:
        """
        Takes key and translates it into predefined language according to its 'vocabulary'.
        @param key: a key for string of text.
        @return: a translated string in defined upon object creation language, falls back to English or simply returns
        the given key if not even fallback in English found.
        """
        localization = getattr(self, self.language, self.en)
        if key in localization:
            return localization[key]

        if key in self.en:
            return self.en[key]

        return key
