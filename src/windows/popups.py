from abc import ABC, abstractmethod
from tkinter import Toplevel, Frame, Entry, Button, END

from src.providers.element import quick_element as qe, random_color
from src.components.filesystem_helper import MusicFileMetadata


class WindowPopup(ABC):
    """
    Abstract class for popup window.
    """
    window: Toplevel
    window_title: str = 'default_window_popup.title'
    window_geometry: str = '300x300'

    def __init__(self):
        """
        Creates a window with its geometry and calls for render of main contents.
        """
        self.window = qe.create_window_popup(self.window_title, self.window_geometry)
        self.render()

    @abstractmethod
    def render(self) -> None:
        """
        This function is called in __init__ and should contain initiation code for all element inside the popup.
        @return: None.
        """
        pass


class WindowMusicConfirm(WindowPopup):
    """
    Class for popup window confirming video metadata.
    """
    window_title: str = 'music_confirm_window.title'

    metadata: MusicFileMetadata

    input_artist: Entry
    input_album: Entry
    input_year: Entry
    input_genre: Entry

    form_complete_callback: type

    def __init__(self, metadata: MusicFileMetadata, form_complete_callback: type):
        """
        Assigns values unique to this form, then calls to father to create a window with its geometry and calls for
        render of main contents.
        @param form_complete_callback: will be called upon form submit.
        """
        self.metadata = metadata
        self.form_complete_callback = form_complete_callback

        super().__init__()

    def render(self) -> None:
        frame = Frame(self.window, bg=random_color())

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(4, weight=1)
        frame.rowconfigure(5, weight=1)
        frame.rowconfigure(7, weight=1)
        frame.rowconfigure(8, weight=1)

        # artist label and input
        qe.create_label(frame, "artist", {"row": 0, "column": 0, 'sticky': 'nw'})
        self.input_artist = qe.create_textbox(frame, self.metadata.artist, {"row": 1, "column": 0, 'sticky': 'nw'})

        # album name label and input
        qe.create_label(frame, "album", {"row": 2, "column": 0, 'sticky': 'nw'})
        self.input_album = qe.create_textbox(frame, self.metadata.album, {"row": 3, "column": 0, 'sticky': 'nw'})

        # swap btn
        swap_btn = Button(frame, text="Swap", font=('Arial', 18), command=self.swap_artist_and_album)
        swap_btn.grid(row=0, column=1, sticky='nw', rowspan=4)

        # year label and input
        qe.create_label(frame, "year", {'row': 4, 'column': 0, 'sticky': 'nw', 'columnspan': 2})
        self.input_year = qe.create_textbox(frame, self.metadata.year,
                                            {'row': 5, 'column': 0, 'sticky': 'nw', 'columnspan': 2})

        # genre label and input
        qe.create_label(frame, "genre", {'row': 6, 'column': 0, 'sticky': 'nw', 'columnspan': 2})
        self.input_genre = qe.create_textbox(frame, self.metadata.genre,
                                             {'row': 7, 'column': 0, 'sticky': 'nw', 'columnspan': 2})

        # submit button
        submit_btn = Button(frame, text="Submit", font=('Arial', 18), command=self.submit)
        submit_btn.grid(row=8, column=0, sticky='nw', columnspan=1)

        frame.pack(fill='x', padx=10, pady=10)

    def swap_artist_and_album(self) -> None:
        """
        Replaces artist input value with album value and vice versa. Acts as a switch for faster mistake correction.
        @return: None.
        """
        artist = self.input_artist.get()
        album = self.input_album.get()

        self.input_artist.delete(0, END)
        self.input_album.delete(0, END)

        self.input_artist.insert(0, album)
        self.input_album.insert(0, artist)

    def submit(self):
        """
        Updates metadata from inputs and calls for complete callback.
        @return: None.
        """
        self.metadata.artist = self.input_artist.get()
        self.metadata.album = self.input_album.get()
        self.metadata.year = self.input_year.get()
        self.metadata.genre = self.input_genre.get()

        self.form_complete_callback(self.metadata)
