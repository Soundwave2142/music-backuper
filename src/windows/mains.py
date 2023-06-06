from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable
from functools import partial
from webbrowser import open_new
from tkinter import Tk, Toplevel, Menu, Frame, Entry, Button

from src.providers.constants import *
from src.providers.config import config
from src.providers.language import translate as __
from src.providers.element import quick_element as qe, random_color
from src.components.processors import ComponentProcessorDownloader


class Window(ABC):
    """
    Base abstract class for any window object
    Attributes:
        window_class: Tk or Toplevel depending on if window is root.
        window:       Default value should be type of the class that needs to be created. in __init__ class Tk or
                      TopLevel object of the window itself is created depending on what type was defined as default.
        window_title: string key for location that will be given to title of window.
        windows:      dictionary of open windows, only filled if there is any open sub-windows.
    """
    window_class: type = Toplevel
    window: Tk | Toplevel
    window_title: str = 'default_window.title'
    windows: dict[str, Window] = {}  # collection of sub-windows that are currently open

    def __init__(self):
        """
        Create window, menubar and call functions to render elements into it.
        """
        self.window = qe.create_window(self.window_class, self.window_title)
        self.menubar = Menu(self.window)

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

    def call_window(self, window_class: type, properties: tuple, close_function: Callable) -> Window:
        """
        A function to create a new window with all the steps for child support.
        @param window_class: class of the window to call.
        @param properties:
        @param close_function: the function to call on window close event.
        @return: None
        """
        if window_class.__name__ in self.windows:
            self.windows[window_class.__name__].window.focus_set()
        else:
            window = window_class(*properties)
            self.windows[window_class.__name__] = window

            window.window.protocol("WM_DELETE_WINDOW", partial(close_function, window))

        return self.windows[window_class.__name__]

    def on_window_close(self, window: Window) -> None:
        """
        This function is called when on of the child windows are closed.
        @param window: object of window that is being closed.
        @return: None.
        """
        self.windows.pop(type(window).__name__, None)
        window.window.destroy()


class WindowAbout(Window):
    """
    Class for window for about section of the app.
    """
    window_class: type = Toplevel
    window_title: str = 'about_window.title'

    def render_root(self):
        """
        Currently does not render anything, future plans include to have some description of the functionality of the
        app.
        @return: None
        """
        pass


class WindowConfig(Window):
    """
    Class for window for configuration of the app.
    """
    window_class: type = Toplevel
    window_title: str = 'config_window.title'

    input_downloader_chapter: Entry = None

    def render_root(self) -> None:
        """
        Renders all elements for app config
        @return: None
        """
        self.render_downloader_config()

    def render_downloader_config(self):
        """
        Renders view for backing up and cleaning section. Current approximate look:

           | ........0..............1...............2....................... |
        0. | section label                                                   |
        1. | from input label | from input | clean up button                 |
        2. | from input error                                                |
        3. | to input label   | to input   | back up button                  |
        4. | to input error                                                  |
           |=================================================================|

        @return: None.
        """
        # create frame with needed amount of columns
        frame = Frame(self.window, bg=random_color())

        frame.columnconfigure(0, weight=1)

        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(4, weight=1)

        qe.create_label(
            frame, 'config_window.downloader_chapter_folder', {"row": 0, "column": 0, 'sticky': 'nw', 'columnspan': 3}
        )

        self.input_downloader_chapter = qe.create_textbox(
            frame, config.get("yt_downloader_chapter_format", ''), {"row": 1, "column": 0, 'sticky': 'nw'}
        )

        frame.pack(fill='x', padx=10, pady=10)


# TODO: describe classes and functions
# TODO: rework this class and move elements to quick element
class WindowRoot(Window):
    """
    Root window, first thing user sees, contains most of the functionality.
    """
    window_class: type = Tk
    window_title: str = 'root_window.title'

    input_path_from = None
    input_path_from_error_label = None
    input_path_to = None
    input_path_to_error_label = None

    input_download_link = None
    input_download_link_error_label = None

    def render_menu(self) -> None:
        """
        Creates a menu-bar element and renders menu for current window.

        Currently, menu looks like this:
        ====================================================================
        | config | theme switch  | language switcher | about section       |
        ====================================================================
        |        | theme default | English           | about functionality |
        |        | theme dark    | Ukrainian         | open git page       |
        |        |               | Norwegian         |                     |
        ====================================================================

        @return: None
        """

        # config button
        self.menubar.add_command(
            label=__('config.label'),
            command=partial(self.call_window, WindowConfig, {}, self.on_window_close)
        )

        # theme switcher
        switch_theme = Menu(self.menubar, tearoff=0)
        switch_theme.add_command(
            label=__('theme.default.label'),
            command=partial(self.config_switcher, 'theme', 'default')
        )
        switch_theme.add_command(
            label=__('theme.default_night.label'),
            command=partial(self.config_switcher, 'theme', 'night')
        )
        self.menubar.add_cascade(menu=switch_theme, label=__('themes.label'))

        # language switcher
        switch_language = Menu(self.menubar, tearoff=0)
        switch_language.add_command(
            label=__('language.en.label'),
            command=partial(self.config_switcher, 'language', 'en')
        )
        switch_language.add_command(
            label=__('language.ua.label'),
            command=partial(self.config_switcher, 'language', 'ua')
        )
        switch_language.add_command(
            label=__('language.no.label'),
            command=partial(self.config_switcher, 'language', 'no')
        )
        self.menubar.add_cascade(menu=switch_language, label=__('languages.label'))

        # about section
        about = Menu(self.menubar, tearoff=0)
        about.add_command(
            label=__('about.functionality.label'),
            command=partial(self.call_window, WindowConfig, {}, self.on_window_close)
        )
        about.add_command(label=__('about.open_git.label'), command=partial(open_new, URL_GITHUB))
        self.menubar.add_cascade(menu=about, label=__('about.label'))

        # pack menu
        self.window.config(menu=self.menubar)

    def render_root(self) -> None:
        """
        Calls functions to render all the sections.
        @return: None.
        """
        self.render_root_section_backup_and_clean()
        self.render_root_section_download()

        self.window.mainloop()

    def render_root_section_backup_and_clean(self) -> None:
        """
        Renders view for backing up and cleaning section. Current approximate look:

           | ........0..............1...............2....................... |
        0. | section label                                                   |
        1. | from input label | from input | clean up button                 |
        2. | from input error                                                |
        3. | to input label   | to input   | back up button                  |
        4. | to input error                                                  |
           |=================================================================|

        @return: None.
        """
        # create frame with needed amount of columns
        frame = Frame(self.window, bg=random_color())

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(4, weight=1)

        # row 0
        qe.create_label(
            frame, 'root_window.clean_and_backup', {"row": 0, "column": 0, 'sticky': 'nw', 'columnspan': 3}
        )

        # row 1
        qe.create_label(frame, "from", {"row": 1, "column": 0, 'sticky': 'nw'})
        self.input_path_from = qe.create_textbox(
            frame,
            config.get(CONFIG_KEY_BACKUPPER_PATH_FROM, ''),
            {"row": 1, "column": 1, 'sticky': 'nw'}
        )
        button = Button(frame, text="Clean up", font=('Arial', 18), command=self.clean_up_director)
        button.grid(row=1, column=2, sticky='nw')

        # row 2
        self.input_path_from_error_label = qe.create_label(
            frame, "", {"row": 1, "column": 2, 'sticky': 'nw', 'columnspan': 3}
        )  # error label

        # row 3
        qe.create_label(frame, "to", {"row": 3, "column": 0, 'sticky': 'nw'})
        self.input_path_to = qe.create_textbox(
            frame,
            config.get(CONFIG_KEY_BACKUPPER_PATH_TO, ''),
            {"row": 3, "column": 1, 'sticky': 'nw'}
        )
        button2 = Button(frame, text="Back Up", font=('Arial', 18), command=self.backup_to_directory)
        button2.grid(row=3, column=2, sticky='nw')

        # row 4
        self.input_path_to_error_label = qe.create_label(
            frame, "", {"row": 4, "column": 1, 'sticky': 'nw', 'columnspan': 3}
        )  # error label

        frame.pack(fill='x', padx=10, pady=10)

    def render_root_section_download(self):
        """
        Renders view for download from YouTube section. Current approximate look:

           | ..........0.................0.............3.................... |
        0. | section label                                                   |
        1. | link input label      | link input | start button               |
        2. | link input validation                                           |
           |=================================================================|

        @return: None.
        """
        frame_download = Frame(self.window, bg=random_color())

        frame_download.columnconfigure(0, weight=1)
        frame_download.columnconfigure(1, weight=1)
        frame_download.columnconfigure(2, weight=1)

        frame_download.rowconfigure(0, weight=1)
        frame_download.rowconfigure(1, weight=1)

        # row 0
        qe.create_label(
            frame_download, 'root_window.download_from_yt',
            {'row': 0, 'column': 0, 'sticky': 'nw', 'columnspan': 3}
        )

        # row 1
        qe.create_label(frame_download, 'root_window.download_input_label', {'row': 1, 'column': 0, 'sticky': 'nw'})
        self.input_download_link = qe.create_textbox(
            frame_download, config.get(CONFIG_KEY_DOWNLOADER_LINK, ''),
            {"row": 1, "column": 1, 'sticky': 'nw'}
        )

        button = Button(frame_download, text="Download", font=('Arial', 18), command=self.download_album)
        button.grid(row=1, column=2, sticky='nw')

        # row 2
        self.input_download_link_error_label = qe.create_label(
            frame_download, "", {"row": 2, "column": 0, 'sticky': 'nw', 'columnspan': 3}
        )

        frame_download.pack(fill='x', padx=10, pady=10)

    def clean_up_director(self) -> None:
        pass  # TODO: implement

    def backup_to_directory(self) -> None:
        pass  # TODO: implement

    def download_album(self) -> None:
        """
        Create processor component, validate and process.
        @return: None.
        """
        downloader = ComponentProcessorDownloader(
            self.input_download_link, self.input_download_link_error_label, self
        )

        if downloader.validate():
            downloader.process()
