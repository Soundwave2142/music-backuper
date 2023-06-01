from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.windows.root import WindowRoot

from src.components.processors.cleaner import ComponentProcessorCleaner
from src.components.processors.backupper import ComponentProcessorBackupper
from src.components.processors.downloader import ComponentProcessorDownloader

from src.components.validator import validate_input, NotEmptyRule, PathExistsRule


# TODO: Rework this class
class ProcessorsOverlordComponent:
    def __init__(self, window: WindowRoot):
        self.window = window

    def validateBackupFromField(self):
        return validate_input(
            self.window.input_path_from,
            self.window.input_path_from_error_label,
            [NotEmptyRule(), PathExistsRule()]
        )

    def validateBackupToField(self):
        return validate_input(
            self.window.input_path_to,
            self.window.input_path_to_error_label,
            [NotEmptyRule(), PathExistsRule()]
        )

    def validateDownloadYouTubeField(self):
        return validate_input(
            self.window.input_download_link,
            self.window.input_download_link_error_label,
            [NotEmptyRule()]
        )

    def cleanup(self):
        if self.validateBackupFromField() is True:
            cleaner = ComponentProcessorCleaner()
            cleaner.process(self.window.input_path_from)

    def backup(self):
        if self.validateBackupFromField() is True and self.validateBackupToField() is True:
            backupper = ComponentProcessorBackupper()
            backupper.process(self.window.input_path_from)

    def download(self):
        if self.validateDownloadYouTubeField():
            downloader = ComponentProcessorDownloader()
            downloader.process()
