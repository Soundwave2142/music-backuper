from src.providers.config import ConfigProvider
from src.providers.element import QuickElementProvider
from src.windows.root import WindowRoot

config = ConfigProvider()
QE = QuickElementProvider(config.get('language', 'en'), config.get('theme', 'default'))

window = WindowRoot(config, QE)
