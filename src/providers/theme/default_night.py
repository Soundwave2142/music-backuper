from dataclasses import dataclass
from src.providers.theme.default import ThemeDefault

THEME_NAME = 'default_night'


@dataclass
class ThemeDefaultNight(ThemeDefault):
    window_configure = {"bg": "#3a3e45"}
