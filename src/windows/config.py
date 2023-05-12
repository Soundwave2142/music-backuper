# outside libs
import tkinter as tk

# classes
from src.providers.config import ConfigProvider
from src.providers.element import QuickElementProvider
from src.windows._abstract import Window


# TODO: describe classes and functions
class WindowConfig(Window):
    def __init__(self, config: ConfigProvider, quick_element: QuickElementProvider):
        self.config = config
        self.QE = quick_element

        self.window = tk.Toplevel()
        self.render_window()

    def render_window(self):
        self.QE.create_window(self.window, 'config_window.title')
