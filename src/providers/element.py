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

    def create_window(self, window, title: str):
        window.geometry(self.theme.window_geometry_size)
        window.title(self.__.t(title))
        window.configure(**self.theme.window_configure)

        return window

    def create_label(self, parent, label: str, grid_config=None) -> tk.Label:
        label = tk.Label(parent, text=self.__.t(label), font=self.theme.font_normal)
        self.__pack_or_grid(label, parent, self.theme.label_pack, grid_config)

        return label

    def create_textbox(self, parent, grid_config=None) -> tk.Entry:
        textbox = tk.Entry(parent, font=self.theme.font_normal)
        self.__pack_or_grid(textbox, parent, {}, grid_config)

        return textbox

    def __pack_or_grid(self, element, parent, pack_config, grid_config):
        if isinstance(parent, tk.Frame):
            element.grid(**grid_config)
        else:
            element.pack(**pack_config)
