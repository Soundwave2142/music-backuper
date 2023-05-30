# outside libs
from tkinter import Toplevel
from src.windows._abstract import Window


class WindowConfig(Window):
    """
    Class for window for configuration of the app.
    """
    window: Toplevel = Toplevel
    window_title: str = 'config_window.title'

    def render_root(self) -> None:
        """
        Currently does not render anything, future plans include to have some of the values like paths and so on.
        @return: None
        """
        pass
