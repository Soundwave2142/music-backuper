from random import randint
import tkinter as tk

from src.providers.language import translate as __
from src.providers.config import config

from src.providers.theme.default import ThemeDefault
from src.providers.theme.default import THEME_NAME as THEME_DEFAULT_NAME
from src.providers.theme.default_night import ThemeDefaultNight
from src.providers.theme.default_night import THEME_NAME as THEME_DEFAULT_NIGHT_NAME


def theme_registry():
    """
    @return: dictionary of the 'theme constant name' to 'class name'
    """
    return {
        THEME_DEFAULT_NAME: ThemeDefault,
        THEME_DEFAULT_NIGHT_NAME: ThemeDefaultNight
    }


def random_color():
    """
    @return: random color in HEX format
    """
    return '#%02X%02X%02X' % (randint(0, 255), randint(0, 255), randint(0, 255))


class __QuickElementProvider:
    """
    Class that is used for quick element creation, used throughout the app to avoid repeating code. Gathers settings
    for elements from given theme.
    """
    theme: ThemeDefault

    def __init__(self, theme_name: str):
        """
        @param theme_name: theme constant name
        """
        self.theme = theme_registry()[theme_name]()

    def create_window(self, window: tk.Tk | tk.Toplevel, title: str) -> tk.Tk | tk.Toplevel:
        """
        Creates a geometry, title and configuration for window element, basic stuff.
        @param window: Tk or Toplevel object of the window itself.
        @param title: string key for translation.
        @return: tk window element that was previously given and modified.
        """
        window.geometry(self.theme.window_geometry_size)
        window.title(__(title))
        window.configure(**self.theme.window_configure)

        return window

    def create_label(self, parent: tk.Frame, string: str, grid_config: dict = None) -> tk.Label:
        """
        Creates a label element.
        @param parent: tk element that acts as parent for object that will be created.
        @param string: actual string of the label.
        @param grid_config: configuration for the element in case of it being inside a Frame, usually something like
        {"row": 1, "column": 1}.
        @return: created Label element of tk.
        """
        label = tk.Label(parent, text=__(string), font=self.theme.font_normal, background=random_color())

        if string:
            label.grid(**grid_config)

        return label

    def create_textbox(self, parent: tk.Frame, grid_config: dict = None) -> tk.Entry:
        """
        Creates a text box element.
        @param parent: tk element that acts as parent for object that will be created.
        @param grid_config: configuration for the element in case of it being inside a Frame, usually something like
        {"row": 1, "column": 1}.
        @return: created Entry element of tk.
        """
        textbox = tk.Entry(parent, font=self.theme.font_normal)
        textbox.grid(**grid_config)

        return textbox

    def show(self, element: tk.Widget, grid_config: dict):
        element.grid(**grid_config)

    def hide(self, element: tk.Widget):
        element.grid_forget()


quick_element = __QuickElementProvider(config.get('theme', 'default'))
