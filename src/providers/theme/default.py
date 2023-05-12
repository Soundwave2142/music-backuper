from dataclasses import dataclass

THEME_NAME = 'default'


@dataclass
class ThemeDefault:
    font_normal = ('Arial', 15)

    label_pack = {"padx": 0, "pady": 0}

    window_geometry_size: str = "800x800"
    window_configure = {"bg": "#deebff"}
