# outside libs
import tkinter as tk
import webbrowser
from functools import partial

# classes
from src.components.processors_overlord import ProcessorsOverlordComponent
from src.providers.config import ConfigProvider
from src.providers.element import QuickElementProvider
from src.windows._abstract import Window
from src.windows.config import WindowConfig

# constants
from src.providers.theme.default import THEME_NAME as THEME_DEFAULT_NAME
from src.providers.theme.default_night import THEME_NAME as THEME_DEFAULT_NIGHT_NAME


# TODO: describe classes and functions
class WindowRoot(Window):
    window: tk.Tk = tk.Tk
    window_title: str = 'root_window.title'

    def __init__(self, config: ConfigProvider, quick_element: QuickElementProvider):
        self.overlord = ProcessorsOverlordComponent(self, quick_element.__)

        self.input_path_from = None
        self.input_path_from_error_label = None
        self.input_path_to = None
        self.input_path_to_error_label = None

        super().__init__(config, quick_element)

    def render_root(self):
        # top label and frame
        self.QE.create_label(self.window, 'root_window.clean_and_backup')

        # create frame with needed amount of columns
        frame = tk.Frame(self.window)
        for count in range(4):
            frame.columnconfigure(count, weight=1)

        # input path from
        self.QE.create_label(frame, "from", {"row": 0, "column": 0})
        self.input_path_from = self.QE.create_textbox(frame, {"row": 0, "column": 1})
        self.input_path_from_error_label = self.QE.create_label(frame, "", {"row": 1, "column": 1})  # error label

        # input path to
        self.QE.create_label(frame, "to", {"row": 2, "column": 0})
        self.input_path_to = self.QE.create_textbox(frame, {"row": 2, "column": 1})
        self.input_path_to_error_label = self.QE.create_label(frame, "", {"row": 3, "column": 1})  # error label

        button = tk.Button(frame, text="Clean up", font=('Arial', 18), command=self.overlord.cleanup)
        button.grid(row=0, column=2)

        button2 = tk.Button(frame, text="Back Up", font=('Arial', 18), command=self.overlord.backup)
        button2.grid(row=1, column=2)

        frame.pack(fill='x')

        self.window.mainloop()

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
            label=self.QE.t('config.label'),
            command=partial(self.call_window, WindowConfig, self.on_window_close)
        )

        # theme switcher
        switch_theme = tk.Menu(self.menubar, tearoff=0)
        switch_theme.add_command(
            label=self.QE.t('theme.default.label'),
            command=partial(self.switch_theme, THEME_DEFAULT_NAME)
        )
        switch_theme.add_command(
            label=self.QE.t('theme.default_night.label'),
            command=partial(self.switch_theme, THEME_DEFAULT_NIGHT_NAME)
        )
        self.menubar.add_cascade(menu=switch_theme, label=self.QE.t('themes.label'))

        # language switcher
        switch_language = tk.Menu(self.menubar, tearoff=0)
        switch_language.add_command(label=self.QE.t('language.en.label'), command=partial(self.switch_language, 'en'))
        switch_language.add_command(label=self.QE.t('language.ua.label'), command=partial(self.switch_language, 'ua'))
        switch_language.add_command(label=self.QE.t('language.no.label'), command=partial(self.switch_language, 'no'))
        self.menubar.add_cascade(menu=switch_language, label=self.QE.t('languages.label'))

        # about section
        about = tk.Menu(self.menubar, tearoff=0)
        about.add_command(
            label=self.QE.t('about.functionality.label'),
            command=partial(self.call_window, WindowConfig, self.on_window_close)
        )
        about.add_command(
            label=self.QE.t('about.open_git.label'),
            command=partial(webbrowser.open_new, "https://github.com/Soundwave2142/music-backuper")
        )
        self.menubar.add_cascade(menu=about, label=self.QE.t('about.label'))

        # pack menu
        self.window.config(menu=self.menubar)

    def switch_theme(self, theme):
        self.config.set("theme", theme)
        self.destroy()

    def switch_language(self, language):
        self.config.set("language", language)
        self.destroy()
