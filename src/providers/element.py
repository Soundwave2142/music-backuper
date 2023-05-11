import tkinter as tk
from src.providers.language import LanguageProvider
from src.providers.theme.default import ThemeDefault
from src.providers.theme.default import THEME_NAME as THEME_DEFAULT_NAME
from src.providers.theme.default_night import ThemeDefaultNight
from src.providers.theme.default_night import THEME_NAME as THEME_DEFAULT_NIGHT_NAME


def theme_registry():
    return {
        THEME_DEFAULT_NAME: ThemeDefault,
        THEME_DEFAULT_NIGHT_NAME: ThemeDefaultNight
    }


class QuickElementProvider:
    # type-hint
    theme: ThemeDefault

    def __init__(self, language, theme):
        self.__ = LanguageProvider(language)
        self.theme = theme_registry()[theme]()

    def t(self, key: str) -> str:
        return self.__.t(key)

    def create_window(self, root, title: str):
        root.geometry(self.theme.window_geometry_size)
        root.title(self.__.t(title))
        root.configure(**self.theme.window_configure)

    def create_label(self, root, label: str):
        label = tk.Label(root, text=label, font=self.theme.font_normal)
        label.pack(**self.theme.label_padding)
