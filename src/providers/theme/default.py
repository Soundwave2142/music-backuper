from dataclasses import dataclass

THEME_NAME = 'default'


@dataclass
class ThemeDefault:
    font_normal = ('Arial', 15)

    label_padding = {"padx": 0, "pady": 0}

    window_geometry_size: str = "500x500"
    window_configure = {"bg": "#deebff"}
