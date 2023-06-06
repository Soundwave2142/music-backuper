from dataclasses import dataclass
from random import randint
from tkinter import Tk, Toplevel, Frame, Widget, Label, Entry

from src.providers.constants import THEME_DEFAULT_NAME, THEME_NIGHT_NAME
from src.providers.language import translate as __
from src.providers.config import config


@dataclass
class ThemeDefault:
    """Default theme config"""
    font_normal = ('Arial', 15)

    label_pack = {"padx": 0, "pady": 0}

    window_geometry_size: str = "800x800"
    window_configure = {"bg": "#deebff"}


@dataclass
class ThemeNight(ThemeDefault):
    """Night theme config, for full list of properties see ThemeDefault"""
    window_configure = {"bg": "#3a3e45"}


def theme_registry():
    """
    @return: dictionary of the 'theme constant name' to 'class name'
    """
    return {
        THEME_DEFAULT_NAME: ThemeDefault,
        THEME_NIGHT_NAME: ThemeNight
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

    def create_window(self, window_class: type, title: str) -> Tk | Toplevel:
        """
        Creates a geometry, title and configuration for window element, basic stuff.
        @param window_class: class, should be Tk or Toplevel.
        @param title: string key for translation.
        @return: tk window element that was previously given and modified.
        """
        window = window_class()
        window.geometry(self.theme.window_geometry_size)
        window.title(__(title))
        window.configure(**self.theme.window_configure)

        return window

    def create_window_popup(self, title: str, geometry_size: str = '300x300') -> Toplevel:
        """
        Creates a window with geometry, title and configuration for window element, basic stuff.
        @param title: string key for translation.
        @param geometry_size: for window size
        @return: tk window element that was previously given and modified.
        """
        window = Toplevel()
        window.geometry(geometry_size)
        window.title(__(title))
        window.configure(**self.theme.window_configure)

        return window

    def create_label(self, parent: Frame, string: str, grid_config: dict = None) -> Label:
        """
        Creates a label element.
        @param parent: tk element that acts as parent for object that will be created.
        @param string: actual string of the label.
        @param grid_config: configuration for the element in case of it being inside a Frame, usually something like
        {"row": 1, "column": 1}.
        @return: created Label element of tk.
        """
        label = Label(parent, text=__(string), font=self.theme.font_normal, background=random_color())

        if string:
            label.grid(**grid_config)

        return label

    def create_textbox(self, parent: Frame, value: str = '', grid_config: dict = None) -> Entry:
        """
        Creates a text box element.
        @param parent: tk element that acts as parent for object that will be created.
        @param value: default value for input.
        @param grid_config: configuration for the element in case of it being inside a Frame, usually something like
        {"row": 1, "column": 1}.
        @return: created Entry element of tk.
        """
        textbox = Entry(parent, font=self.theme.font_normal)
        textbox.insert(0, value)
        textbox.grid(**grid_config)

        return textbox

    def show(self, element: Widget, grid_config: dict):
        element.grid(**grid_config)

    def hide(self, element: Widget):
        element.grid_forget()


quick_element = __QuickElementProvider(config.get('theme', THEME_DEFAULT_NAME))
