# outside libs
from tkinter import Tk, Menu, Frame, Button
from webbrowser import open_new
from functools import partial

# libs
from src.providers.element import quick_element as qe, random_color
from src.providers.language import translate as __

# classes
from src.components.processors_overlord import ProcessorsOverlordComponent
from src.windows._abstract import Window
from src.windows.config import WindowConfig

# constants
from src.providers.theme.default import THEME_NAME as THEME_DEFAULT_NAME
from src.providers.theme.default_night import THEME_NAME as THEME_DEFAULT_NIGHT_NAME

URL_GITHUB = "https://github.com/Soundwave2142/music-backuper"  # TODO: move


# TODO: describe classes and functions
class WindowRoot(Window):
    """
    Root window, first thing user sees, contains most of the functionality.
    """
    window_class: type = Tk
    window_title: str = 'root_window.title'

    overlord: ProcessorsOverlordComponent

    input_path_from = None
    input_path_from_error_label = None
    input_path_to = None
    input_path_to_error_label = None

    input_download_link = None
    input_download_link_error_label = None

    def __init__(self):
        self.overlord = ProcessorsOverlordComponent(self)
        super().__init__()

    def render_menu(self) -> None:
        """
        Creates a menubar element and renders menu for current window.

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
            command=partial(self.call_window, WindowConfig, self.on_window_close)
        )

        # theme switcher
        switch_theme = Menu(self.menubar, tearoff=0)
        switch_theme.add_command(
            label=__('theme.default.label'),
            command=partial(self.config_switcher, 'theme', THEME_DEFAULT_NAME)
        )
        switch_theme.add_command(
            label=__('theme.default_night.label'),
            command=partial(self.config_switcher, 'theme', THEME_DEFAULT_NIGHT_NAME)
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
            command=partial(self.call_window, WindowConfig, self.on_window_close)
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
        self.input_path_from = qe.create_textbox(frame, {"row": 1, "column": 1, 'sticky': 'nw'})
        button = Button(frame, text="Clean up", font=('Arial', 18), command=self.overlord.cleanup)
        button.grid(row=1, column=2, sticky='nw')

        # row 2
        self.input_path_from_error_label = qe.create_label(
            frame, "", {"row": 1, "column": 2, 'sticky': 'nw', 'columnspan': 3}
        )  # error label

        # row 3
        qe.create_label(frame, "to", {"row": 3, "column": 0, 'sticky': 'nw'})
        self.input_path_to = qe.create_textbox(frame, {"row": 3, "column": 1, 'sticky': 'nw'})
        button2 = Button(frame, text="Back Up", font=('Arial', 18), command=self.overlord.backup)
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
        qe.create_label(frame_download, 'root_window.download_input_label',{'row': 1, 'column': 0, 'sticky': 'nw'})
        self.input_download_link = qe.create_textbox(frame_download, {"row": 1, "column": 1, 'sticky': 'nw'})

        button = Button(frame_download, text="Download", font=('Arial', 18), command=self.overlord.download)
        button.grid(row=1, column=2, sticky='nw')

        # row 2
        self.input_download_link_error_label = qe.create_label(
            frame_download, "", {"row": 2, "column": 0, 'sticky': 'nw', 'columnspan': 3}
        )

        frame_download.pack(fill='x', padx=10, pady=10)
