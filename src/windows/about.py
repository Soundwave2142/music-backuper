from tkinter import Toplevel
from src.windows._abstract import Window


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
