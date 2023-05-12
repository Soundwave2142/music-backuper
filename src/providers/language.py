class LanguageProvider:
    en = {
        'root_window.title': "SLT v1.0.0",
        'root_window.clean_and_backup': "Clean up folders and back them up to external hard-drive",

        'root_window.download_yt_album': "Download youtube album and split it to m4a files"
    }

    no = {
        'root_window.clean_and_backup': "Rydd opp i mapper og ta sikkerhetskopi av dem på ekstern harddisk.",
        # add at some point for shit and giggles
    }

    def __init__(self, language: str = "en"):
        self.language = language

    def t(self, key: str) -> str:
        localization = getattr(self, self.language, self.en)
        if key in localization:
            return localization[key]

        if key in self.en:
            return self.en[key]

        return key
