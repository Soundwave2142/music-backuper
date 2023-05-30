from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.windows.root import WindowRoot

from src.components.processors.cleaner import ComponentProcessorCleaner
from src.components.processors.backupper import ComponentProcessorBackupper

from src.components.validator import ValidatorComponent, NotEmptyRule, PathDoNotExistsRule
from src.providers.language import LanguageProvider


# TODO: Rework this class
class ProcessorsOverlordComponent:
    def __init__(self, window: WindowRoot, language_provider: LanguageProvider):
        self.window = window
        self.validator = ValidatorComponent(language_provider)

    def validateBackupFromField(self):
        return self.validator.validate_input(
            self.window.input_path_from,
            self.window.input_path_from_error_label,
            [NotEmptyRule(), PathDoNotExistsRule()]
        )

    def validateBackupToField(self):
        return self.validator.validate_input(
            self.window.input_path_to,
            self.window.input_path_to_error_label,
            [NotEmptyRule(), PathDoNotExistsRule()]
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
        pass
