# outside libs
import tkinter as tk
import webbrowser
from functools import partial

# classes
from src.providers.config import ConfigProvider
from src.providers.element import QuickElementProvider
from src.windows._abstract import Window
from src.windows.config import WindowConfig

# constants
from src.providers.theme.default import THEME_NAME as THEME_DEFAULT_NAME
from src.providers.theme.default_night import THEME_NAME as THEME_DEFAULT_NIGHT_NAME


# TODO: describe classes and functions
class WindowRoot(Window):
    def __init__(self):
        self.config = ConfigProvider()
        self.QE = QuickElementProvider(self.config.get('language', 'en'), self.config.get('theme', 'default'))

        self.windows = {}
        self.window = tk.Tk()
        self.menubar = tk.Menu(self.window)

        self.render_root()

    def render_root(self):
        # window and menu
        self.QE.create_window(self.window, 'root_window.title')
        self.render_menu()

        # top label and frame
        self.QE.create_label(self.window, 'root_window.clean_and_backup')

        # create frame with needed amount of columns
        frame = tk.Frame(self.window)
        for count in range(3):
            frame.columnconfigure(count, weight=1)

        self.QE.create_label(frame, "from", {"row": 0, "column": 0})
        self.QE.create_textbox(frame, {"row": 0, "column": 1})

        self.QE.create_label(frame, "to", {"row": 1, "column": 0})
        textbox2 = tk.Entry(frame, font=('Arial', 15))
        textbox2.grid(row=1, column=1)

        button = tk.Button(frame, text="Clean up", font=('Arial', 18))
        button.grid(row=0, column=2)

        button2 = tk.Button(frame, text="Back Up", font=('Arial', 18))
        button2.grid(row=1, column=2)

        frame.pack(fill='x')

        self.window.mainloop()

    def render_menu(self):
        self.menubar = tk.Menu(self.window)

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
            command=partial(self.call_external, "https://github.com/Soundwave2142/music-backuper")
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

    def destroy(self):
        # TODO: add checks asking - are you sure?

        self.window.destroy()
        self.__init__()

    def call_external(self, url):
        webbrowser.open_new(url)

    def call_window(self, window_class: type, window_close_function: type):
        if window_class.__name__ in self.windows:
            self.windows[window_class.__name__].window.focus_set()
        else:
            window = window_class(self.config, self.QE)
            self.windows[window_class.__name__] = window

            window.window.protocol("WM_DELETE_WINDOW", partial(window_close_function, window))

    def on_window_close(self, window: Window):
        self.windows.pop(type(window).__name__, None)
        window.window.destroy()
