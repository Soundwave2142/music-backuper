from __future__ import annotations
from abc import ABC, abstractmethod
from functools import partial

from tkinter import Tk
from tkinter import Toplevel
from tkinter import Menu

from src.providers.config import config
from src.providers.element import quick_element as qe


class Window(ABC):
    """
    Base abstract class for any window object
    Attributes:
        window:       Default value should be type of the class that needs to be created. in __init__ class Tk or
                      TopLevel object of the window itself is created depending on what type was defined as default.
        window_title: string key for location that will be given to title of window.
        windows:      dictionary of open windows, only filled if there is any open sub-windows.
    """
    window_class: type = Toplevel
    window: Tk | Toplevel = None
    window_title: str = 'default_window.title'
    windows: dict[str, Window] = {}  # collection of sub-windows that are currently open

    def __init__(self):
        self.window = self.window_class()
        self.menubar = Menu(self.window)

        # create window and render menu + main window contents
        qe.create_window(self.window, self.window_title)
        self.render_menu()
        self.render_root()

    @abstractmethod
    def render_root(self) -> None:
        """
        This function is called in __init__ and should contain code of initiation of all element inside the window.
        @return: None.
        """
        pass

    def render_menu(self) -> None:
        """
        This function is called in __init__ and should contain code for menu initiation
        @return: None
        """
        pass

    def re_render(self) -> None:
        """
        Destroys current window and re-creates it.
        @return: None.
        """
        # TODO: add checks asking - are you sure?

        self.window.destroy()
        self.__init__()

    def config_switcher(self, name: str, value: str) -> None:
        """
        Acts as switch, for example for switching language or theme. Sets a value to config and re-renders current
        window.
        @param name: config value name.
        @param value: config value.
        @return: None.
        """
        config.set(name, value)
        self.re_render()

    def call_window(self, window_class: type, window_close_function: type) -> None:
        """
        A function to create a new window with all the steps for child support.
        @param window_class: class of the window to call.
        @param window_close_function: the function to call on window close event.
        @return: None
        """
        if window_class.__name__ in self.windows:
            self.windows[window_class.__name__].window.focus_set()
        else:
            window = window_class()
            self.windows[window_class.__name__] = window

            window.window.protocol("WM_DELETE_WINDOW", partial(window_close_function, window))

    def on_window_close(self, window: Window) -> None:
        """
        This function is called when on of the child windows are closed.
        @param window: object of window that is being closed.
        @return: None.
        """
        self.windows.pop(type(window).__name__, None)
        window.window.destroy()
