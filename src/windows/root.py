# outside libs
import tkinter as tk
from functools import partial

# classes
from src.providers.config import ConfigProvider
from src.providers.element import QuickElementProvider

# constants
from src.providers.theme.default import THEME_NAME as THEME_DEFAULT_NAME
from src.providers.theme.default_night import THEME_NAME as THEME_DEFAULT_NIGHT_NAME


# TODO: describe classes and functions
class WindowRoot:
    def __init__(self):
        self.config = ConfigProvider()
        self.QE = QuickElementProvider(self.config.get('language', 'en'), self.config.get('theme', 'default'))

        self.root = tk.Tk()
        self.menubar = tk.Menu(self.root)

        self.render_root()

    def render_root(self):
        self.QE.create_window(self.root, 'root_window.title')
        self.render_menu()

        # TODO: clean up and develop
        self.QE.create_label(self.root, "back up your music")

        textbox = tk.Entry(self.root, font=('Arial', 15))
        textbox.pack(padx=20, pady=20)

        button = tk.Button(self.root, text="Back Up", font=('Arial', 18))
        button.pack(padx=10, pady=10)

        frame = tk.Frame(self.root)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        button = tk.Button(frame, text="Settings", font=('Arial', 18), command=self.call_settings)
        button.pack(padx=10, pady=10)

        self.root.mainloop()

    def render_menu(self):
        self.menubar = tk.Menu(self.root)

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

        self.root.config(menu=self.menubar)

    def switch_theme(self, theme):
        self.config.set("theme", theme)
        self.destroy()

    def switch_language(self, language):
        self.config.set("language", language)
        self.destroy()

    def destroy(self):
        # TODO: add checks asking - are you sure?

        self.root.destroy()
        self.__init__()

    def call_settings(self):
        print('dummy')
